from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api import deps
from app.schemas.schemas import RegistrationRequestCreate, RegistrationRequestResponse
from app.services.registration_service import RegistrationService
from app.models.models import UserRole

router = APIRouter()

@router.post("/request", response_model=RegistrationRequestResponse)
def submit_registration_request(
    *,
    db: Session = Depends(deps.get_db),
    request_in: RegistrationRequestCreate
) -> any:
    """
    Submit a new registration request from a secure token.
    This does NOT create a user. It captures an intake application.
    """
    return RegistrationService.create_request(session=db, req_in=request_in)

@router.get("/request", response_model=List[RegistrationRequestResponse])
def list_registration_requests(
    db: Session = Depends(deps.get_db),
    site_id: Optional[str] = None,
    company_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user = Depends(deps.get_current_active_user)
) -> any:
    """
    List registration requests. Subject to authorization based on caller's role and scope.
    """
    # Assuming basic check, realistically this needs role-based filters
    if current_user.role not in [UserRole.SYSTEM_ADMIN, UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER, UserRole.OPERATIONS_MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions to view registration requests.")
        
    return RegistrationService.list_requests(
        session=db,
        site_id=site_id,
        company_id=company_id,
        status=status
    )

@router.get("/request/{request_id}", response_model=RegistrationRequestResponse)
def get_registration_request(
    request_id: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> any:
    """
    Get a specific registration request by ID.
    """
    if current_user.role not in [UserRole.SYSTEM_ADMIN, UserRole.COMPANY_ADMIN, UserRole.SITE_MANAGER, UserRole.OPERATIONS_MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions to view registration requests.")
        
    return RegistrationService.get_request(session=db, request_id=request_id)
