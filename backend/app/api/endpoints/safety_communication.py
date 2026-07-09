from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.safety_communication_service import SafetyCommunicationService

router = APIRouter()

@router.post("", response_model=schemas.CommunicationResponse)
def create_communication_draft(
    payload: schemas.CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.manage"))
):
    """
    Creates a new safety communication draft.
    """
    return SafetyCommunicationService.create_draft(db, current_user.company_id, current_user.id, payload)

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
    return SafetyCommunicationService.publish(db, current_user.company_id, communication_id, current_user.id, payload.reason)

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
    return SafetyCommunicationService.archive(db, current_user.company_id, communication_id, current_user.id, payload.reason)

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
    return SafetyCommunicationService.acknowledge(db, current_user.company_id, communication_id, current_user.id)

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
    return SafetyCommunicationService.list_communications(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.CommunicationDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("communication.manage"))
):
    """
    Gets dashboard summary of communications.
    """
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
    return SafetyCommunicationService.get_communication(db, current_user.company_id, communication_id)
