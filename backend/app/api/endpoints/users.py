from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user, RoleChecker
from app.models.models import UserRole, WorkerStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SUPERVISOR]))
):
    query = db.query(User)
    if current_user.company_id:
        query = query.filter(User.company_id == current_user.company_id)
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/pending", response_model=List[schemas.UserResponse])
def get_pending_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    query = db.query(User).filter(User.status == WorkerStatus.PENDING)
    if current_user.company_id:
        query = query.filter(User.company_id == current_user.company_id)
    users = query.all()
    return users

def _update_worker_status(user_id: str, status: WorkerStatus, is_active: bool, db: Session, admin: User):
    query = db.query(User).filter(User.id == user_id)
    if admin.company_id:
        query = query.filter(User.company_id == admin.company_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or access denied")
    user.status = status
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    logger.info(f"Admin {admin.id} changed user {user_id} status to {status.value}")
    return user

@router.put("/{user_id}/approve", response_model=schemas.UserResponse)
def approve_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return _update_worker_status(user_id, WorkerStatus.APPROVED, True, db, current_user)

@router.put("/{user_id}/reject", response_model=schemas.UserResponse)
def reject_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return _update_worker_status(user_id, WorkerStatus.REJECTED, False, db, current_user)

@router.put("/{user_id}/suspend", response_model=schemas.UserResponse)
def suspend_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return _update_worker_status(user_id, WorkerStatus.SUSPENDED, False, db, current_user)

@router.put("/{user_id}/reactivate", response_model=schemas.UserResponse)
def reactivate_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return _update_worker_status(user_id, WorkerStatus.APPROVED, True, db, current_user)
