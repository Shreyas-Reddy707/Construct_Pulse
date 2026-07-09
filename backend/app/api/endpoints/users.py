from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user, get_current_user_allow_pending, RoleChecker
from app.models.models import UserRole, WorkerStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

from app.api.deps import get_current_user, get_current_user_allow_pending, RoleChecker, get_current_tenant, PermissionChecker

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    status: WorkerStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SUPERVISOR])),
    tenant = Depends(get_current_tenant)
):
    query = db.query(User).filter(User.role == UserRole.WORKER)
    query = query.filter(User.company_id == tenant.id)
    if status:
        query = query.filter(User.status == status)
    users = query.offset(skip).limit(limit).all()
    return users


@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: User = Depends(get_current_user_allow_pending)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]))
):
    query = db.query(User).filter(User.id == user_id)
    if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
        query = query.filter(User.company_id == current_user.company_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

from app.services.worker_readiness_service import WorkerReadinessService

@router.get("/{user_id}/readiness", response_model=schemas.WorkerReadinessResponse)
def get_worker_readiness(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN, UserRole.SITE_MANAGER]))
):
    query = db.query(User).filter(User.id == user_id)
    if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
        query = query.filter(User.company_id == current_user.company_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return WorkerReadinessService.evaluate_worker_readiness(user)

@router.get("/{user_id}/sites", response_model=List[schemas.SiteResponse])
def get_user_sites(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]))
):
    query = db.query(User).filter(User.id == user_id)
    if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
        query = query.filter(User.company_id == current_user.company_id)
    user = query.first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user.assigned_sites

def _update_worker_status(user_id: str, status: WorkerStatus, is_active: bool, db: Session, admin: User):
    if user_id == admin.id and status == WorkerStatus.SUSPENDED:
        raise HTTPException(status_code=400, detail="Cannot suspend yourself")
        
    query = db.query(User).filter(User.id == user_id)
    if admin.company_id:
        query = query.filter(User.company_id == admin.company_id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or access denied")
        
    if status == WorkerStatus.SUSPENDED and user.role in [UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=400, detail="Admin users cannot be suspended")

    if status == WorkerStatus.APPROVED and user.status == WorkerStatus.PENDING:
        missing_fields = []
        if not user.emergency_contact_name:
            missing_fields.append("emergency contact name")
        if not user.emergency_contact_phone:
            missing_fields.append("emergency contact phone")
        if not user.designation:
            missing_fields.append("designation")
            
        if missing_fields:
            missing_str = ", ".join(missing_fields)
            raise HTTPException(
                status_code=400, 
                detail=f"Worker missing required fields for approval: {missing_str}."
            )

    # If suspending, auto-checkout any active attendance sessions
    if status == WorkerStatus.SUSPENDED:
        from app.models.models import Attendance, AttendanceStatus
        from datetime import datetime, timezone
        active_sessions = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == AttendanceStatus.CHECKED_IN
        ).all()
        for session in active_sessions:
            session.status = AttendanceStatus.CHECKED_OUT
            session.check_out_time = datetime.now(timezone.utc)

    user.status = status
    user.is_active = is_active
    db.refresh(user)
    logger.info(f"Admin {admin.id} changed user {user_id} status to {status.value}")
    return user

@router.put("/{user_id}/approve", response_model=schemas.UserResponse)
def approve_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.approve"))):
    return _update_worker_status(user_id, WorkerStatus.APPROVED, True, db, current_user)

@router.put("/{user_id}/reject", response_model=schemas.UserResponse)
def reject_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.reject"))):
    return _update_worker_status(user_id, WorkerStatus.REJECTED, False, db, current_user)

@router.put("/{user_id}/suspend", response_model=schemas.UserResponse)
def suspend_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.suspend"))):
    return _update_worker_status(user_id, WorkerStatus.SUSPENDED, False, db, current_user)

@router.put("/{user_id}/reactivate", response_model=schemas.UserResponse)
def reactivate_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.reactivate"))):
    return _update_worker_status(user_id, WorkerStatus.APPROVED, True, db, current_user)
