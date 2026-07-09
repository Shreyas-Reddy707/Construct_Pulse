from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole, WorkerStatus
from app.api.deps import get_current_user, get_current_user_allow_pending, RoleChecker, get_current_tenant, PermissionChecker
from app.services.user_service import UserService
from app.services.worker_readiness_service import WorkerReadinessService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    status: WorkerStatus = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SUPERVISOR])),
    tenant = Depends(get_current_tenant)
):
    return UserService.get_users(db, tenant, status, skip, limit)


@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: User = Depends(get_current_user_allow_pending)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]))
):
    return UserService.get_user(db, user_id, current_user)


@router.get("/{user_id}/readiness", response_model=schemas.WorkerReadinessResponse)
def get_worker_readiness(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN, UserRole.SITE_MANAGER]))
):
    user = UserService.get_user(db, user_id, current_user)
    return WorkerReadinessService.evaluate_worker_readiness(user)

@router.get("/{user_id}/sites", response_model=List[schemas.SiteResponse])
def get_user_sites(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]))
):
    return UserService.get_user_sites(db, user_id, current_user)

@router.put("/{user_id}/approve", response_model=schemas.UserResponse)
def approve_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.approve"))):
    return UserService.update_worker_status(db, user_id, WorkerStatus.APPROVED, True, current_user)

@router.put("/{user_id}/reject", response_model=schemas.UserResponse)
def reject_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.reject"))):
    return UserService.update_worker_status(db, user_id, WorkerStatus.REJECTED, False, current_user)

@router.put("/{user_id}/suspend", response_model=schemas.UserResponse)
def suspend_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.suspend"))):
    return UserService.update_worker_status(db, user_id, WorkerStatus.SUSPENDED, False, current_user)

@router.put("/{user_id}/reactivate", response_model=schemas.UserResponse)
def reactivate_worker(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("worker.reactivate"))):
    return UserService.update_worker_status(db, user_id, WorkerStatus.APPROVED, True, current_user)
