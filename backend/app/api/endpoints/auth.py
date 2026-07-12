from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole, WorkerStatus
from app.core.security import verify_firebase_token, create_access_token
from app.core.config import settings
from app.core.utils import normalize_phone_number
import logging
import os
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)

DEMO_AUTH = settings.DEMO_AUTH

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.FirebaseLogin, db: Session = Depends(get_db)):
    """
    Login using Firebase ID token or Demo token.
    Both flows use exactly the same normalization and lookup strategy.
    """
    phone_number = None
    firebase_uid = None
    
    if DEMO_AUTH and login_data.token.startswith("DEMO_TOKEN_"):
        raw_phone = login_data.token.replace("DEMO_TOKEN_", "")
        phone_number = normalize_phone_number(raw_phone)
        firebase_uid = f"demo_uid_{phone_number}"
    else:
        decoded = verify_firebase_token(login_data.token)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        firebase_uid = decoded.get("uid")
        raw_phone = decoded.get("phone_number")
        if raw_phone:
            phone_number = normalize_phone_number(raw_phone)
        
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if not user and phone_number:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            # Sync UID if not already synced
            if user.firebase_uid != firebase_uid:
                user.firebase_uid = firebase_uid
                db.commit()

    if not user:
        raise HTTPException(status_code=404, detail="User not registered")
        
    # Security Rule: Suspended or inactive users should be denied
    if user.status in [WorkerStatus.REJECTED]:
        raise HTTPException(status_code=403, detail="Account rejected")
        
    if not user.is_active and user.status != WorkerStatus.PENDING:
        raise HTTPException(status_code=403, detail="Account suspended")
    
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

class RegisterWorkerRequest(BaseModel):
    first_name: str
    last_name: str
    phone: str
    company_id: str
    department_id: str
    contractor_id: Optional[str] = None
    designation: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

@router.post("/register")
def register_worker(request: RegisterWorkerRequest, db: Session = Depends(get_db)):
    """
    Registers a new worker.
    Normalizes the incoming phone and firmly rejects duplicate registrations.
    """
    normalized_phone = normalize_phone_number(request.phone)
    full_name = f"{request.first_name} {request.last_name}"
    
    # Strictly prevent duplicates by phone number
    user = db.query(User).filter(User.phone_number == normalized_phone).first()
    if user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
        
    firebase_uid = f"demo_uid_{normalized_phone}" if DEMO_AUTH else f"firebase_{normalized_phone}"
    
    # Strictly prevent duplicates by firebase_uid just in case
    uid_user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if uid_user:
        raise HTTPException(status_code=400, detail="Identity already registered")
    
    new_user = User(
        name=full_name,
        phone_number=normalized_phone,
        role=UserRole.WORKER,
        firebase_uid=firebase_uid,
        company_id=request.company_id,
        department_id=request.department_id,
        contractor_id=request.contractor_id,
        is_active=True if DEMO_AUTH else False,
        status=WorkerStatus.APPROVED if DEMO_AUTH else WorkerStatus.PENDING
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(new_user.id)
    return {
        "user_id": str(new_user.id),
        "status": "success",
        "access_token": access_token
    }
