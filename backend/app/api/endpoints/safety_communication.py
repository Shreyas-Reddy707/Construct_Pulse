from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.safety_communication_service import SafetyCommunicationService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, resource_company_id: str):
    if current_user.role == UserRole.SYSTEM_ADMIN:
        return
    if not current_user.company_id or current_user.company_id != resource_company_id:
        raise HTTPException(status_code=403, detail="Tenant isolation violation")

@router.post("", response_model=schemas.CommunicationResponse)
def create_communication_draft(
    payload: schemas.CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.manage"))
):
    """
    Creates a new safety communication draft.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyCommunicationService.create_draft(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{communication_id}/publish", response_model=schemas.CommunicationResponse)
def publish_communication(
    communication_id: str,
    payload: schemas.PublishCommunicationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.publish"))
):
    """
    Publishes a safety communication.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyCommunicationService.publish(db, current_user.company_id, communication_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{communication_id}/archive", response_model=schemas.CommunicationResponse)
def archive_communication(
    communication_id: str,
    payload: schemas.ArchiveCommunicationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.manage"))
):
    """
    Archives a safety communication.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyCommunicationService.archive(db, current_user.company_id, communication_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{communication_id}/acknowledge", response_model=schemas.CommunicationResponse)
def acknowledge_communication(
    communication_id: str,
    payload: schemas.AcknowledgeCommunicationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Acknowledges a safety communication.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return SafetyCommunicationService.acknowledge(db, current_user.company_id, communication_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.CommunicationResponse])
def list_communications(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists safety communications.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    return SafetyCommunicationService.list_communications(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.CommunicationDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.manage"))
):
    """
    Gets dashboard summary of safety communications.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return SafetyCommunicationService.dashboard(db, current_user.company_id)

@router.get("/{communication_id}", response_model=schemas.CommunicationResponse)
def get_communication(
    communication_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets details of a specific safety communication.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    communication = SafetyCommunicationService.get_communication(db, current_user.company_id, communication_id)
    if not communication:
        raise HTTPException(status_code=404, detail="Communication not found")
    return communication
