from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import User, UserRole
from app.schemas import schemas
from app.api.deps import get_current_user, RoleChecker, get_current_tenant
from app.services.approval_service import ApprovalService

router = APIRouter()

@router.get("/pending", response_model=schemas.PaginatedResponse[schemas.RegistrationRequestResponse])
def get_pending_registrations(
    query: schemas.RegistrationQuery = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER])),
    tenant = Depends(get_current_tenant)
):
    """
    Get registration requests for the manager's company.
    """
    items, total = ApprovalService.fetch_pending_requests(db, tenant.id, query)
    return schemas.PaginatedResponse.create(data=items, total_records=total, skip=query.skip, limit=query.limit)

@router.get("/{request_id}", response_model=schemas.RegistrationRequestResponse)
def get_registration(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER])),
    tenant = Depends(get_current_tenant)
):
    """
    Get specific registration request details.
    """
    return ApprovalService.get_request(db, request_id, tenant.id)

@router.post("/{request_id}/under-review", response_model=schemas.RegistrationRequestResponse)
def move_to_under_review(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER]))
):
    """
    Move a registration request to UNDER_REVIEW status.
    """
    return ApprovalService.move_to_under_review(db, request_id, current_user)

@router.post("/{request_id}/approve", response_model=schemas.UserResponse)
def approve_registration(
    request_id: str,
    body: schemas.RegistrationReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER]))
):
    """
    Approve a registration request and activate the identity.
    """
    return ApprovalService.approve_request(db, request_id, current_user, notes=body.notes)

@router.post("/{request_id}/reject", response_model=schemas.RegistrationRequestResponse)
def reject_registration(
    request_id: str,
    body: schemas.RegistrationReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER]))
):
    """
    Reject a registration request.
    """
    return ApprovalService.reject_request(db, request_id, current_user, notes=body.notes)
