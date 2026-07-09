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
    phone_number = None
    if DEMO_AUTH and login_data.token.startswith("DEMO_TOKEN_"):
        phone_number = login_data.token.replace("DEMO_TOKEN_", "")
        firebase_uid = f"demo_uid_{phone_number}"
    else:
        decoded = verify_firebase_token(login_data.token)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        firebase_uid = decoded.get("uid")
        phone_number = decoded.get("phone_number")
        
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if not user and phone_number:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            user.firebase_uid = firebase_uid

    if not user:
        raise HTTPException(status_code=404, detail="User not registered")
    
    if user.status == WorkerStatus.PENDING:
        raise HTTPException(status_code=403, detail="Your account is awaiting company approval.")
    elif user.status == WorkerStatus.REJECTED:
        raise HTTPException(status_code=403, detail="Your account has been rejected.")
    elif user.status == WorkerStatus.SUSPENDED:
        raise HTTPException(status_code=403, detail="Your account has been suspended. Contact your administrator.")
    elif user.status != WorkerStatus.APPROVED:
        raise HTTPException(status_code=403, detail="Your account is not approved.")
    
    import uuid
    from datetime import datetime
    from app.models.models import Session as AuthSession
    
    session_id = str(uuid.uuid4())
    new_session = AuthSession(
        id=session_id,
        user_id=user.id,
        login_time=datetime.utcnow(),
        last_activity=datetime.utcnow()
    )
    db.add(new_session)

    claims = {
        "company_id": user.company_id,
        "role_id": user.role.value if user.role else UserRole.WORKER.value,
        "permission_version": "1.0",
        "session_id": session_id
    }
    
    access_token = create_access_token(user.id, claims=claims)
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

@router.post("/register", deprecated=True)
def register_worker(request: RegisterWorkerRequest, db: Session = Depends(get_db)):
    """
    [DEPRECATED] Legacy direct user creation endpoint.
    New clients must use the Registration Intake workflow (POST /api/v1/register/request).
    This endpoint remains for backwards compatibility only.
    """
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
        is_active=False,
        status=WorkerStatus.PENDING,
        designation=request.designation,
        emergency_contact_name=request.emergency_contact_name,
        emergency_contact_phone=request.emergency_contact_phone
    )
    db.add(new_user)
    db.refresh(new_user)
    
    import uuid
    from datetime import datetime
    from app.models.models import Session as AuthSession
    
    session_id = str(uuid.uuid4())
    new_session = AuthSession(
        id=session_id,
        user_id=new_user.id,
        login_time=datetime.utcnow(),
        last_activity=datetime.utcnow()
    )
    db.add(new_session)

    claims = {
        "company_id": new_user.company_id,
        "role_id": new_user.role.value if new_user.role else UserRole.WORKER.value,
        "permission_version": "1.0",
        "session_id": session_id
    }
    
    access_token = create_access_token(new_user.id, claims=claims)
    return {
        "user_id": str(new_user.id),
        "status": "success",
        "access_token": access_token
    }


