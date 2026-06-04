from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.core.security import verify_firebase_token, create_access_token

router = APIRouter()

import os
from pydantic import BaseModel
from typing import Optional
from app.models.models import UserRole, WorkerStatus
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
logger.info(f"DEMO_AUTH={settings.DEMO_AUTH}")

DEMO_AUTH = settings.DEMO_AUTH

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.FirebaseLogin, db: Session = Depends(get_db)):
    """
    Login using Firebase ID token
    """
    if DEMO_AUTH and login_data.token.startswith("DEMO_TOKEN_"):
        phone_number = login_data.token.replace("DEMO_TOKEN_", "")
        firebase_uid = f"demo_uid_{phone_number}"
    else:
        decoded = verify_firebase_token(login_data.token)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        firebase_uid = decoded.get("uid")
        
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")
    
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

class RegisterWorkerRequest(BaseModel):
    first_name: str
    last_name: str
    phone: str
    company_id: str
    department_id: str
    contractor_id: Optional[str] = None
    designation: str
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

@router.post("/register")
def register_worker(request: RegisterWorkerRequest, db: Session = Depends(get_db)):
    full_name = f"{request.first_name} {request.last_name}"
    user = db.query(User).filter(User.phone_number == request.phone).first()
    if user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
        
    firebase_uid = f"demo_uid_{request.phone}" if DEMO_AUTH else f"firebase_{request.phone}"
    
    new_user = User(
        name=full_name,
        phone_number=request.phone,
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


