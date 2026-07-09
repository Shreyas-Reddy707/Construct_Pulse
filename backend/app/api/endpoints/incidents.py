from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.incident_service import IncidentService

router = APIRouter()

@router.post("", response_model=schemas.IncidentResponse)
def create_incident(
    payload: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new incident report. Workers and above can create incidents.
    """
    return IncidentService.create_incident(db, current_user.company_id, current_user.id, payload)

@router.get("", response_model=List[schemas.IncidentResponse])
def list_incidents(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Lists incidents within the tenant.
    """
    return IncidentService.list_incidents(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.IncidentDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Returns incident operational counts.
    """
    return IncidentService.dashboard(db, current_user.company_id)

@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    return IncidentService.get_incident(db, current_user.company_id, incident_id)

@router.post("/{incident_id}/assign", response_model=schemas.IncidentResponse)
def assign_investigator(
    incident_id: str,
    payload: schemas.IncidentAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Assign an investigator to the incident.
    """
    return IncidentService.assign_investigator(db, current_user.company_id, incident_id, current_user.id, payload)

@router.post("/{incident_id}/status", response_model=schemas.IncidentResponse)
def update_status(
    incident_id: str,
    payload: schemas.IncidentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Update the incident status.
    """
    return IncidentService.update_status(db, current_user.company_id, incident_id, current_user.id, payload)

@router.post("/{incident_id}/participants", response_model=schemas.IncidentParticipantResponse)
def add_participant(
    incident_id: str,
    payload: schemas.IncidentParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Add a participant (witness, involved party) to an incident.
    """
    return IncidentService.add_participant(db, current_user.company_id, incident_id, current_user.id, payload)

@router.get("/{incident_id}/participants", response_model=List[schemas.IncidentParticipantResponse])
def get_participants(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Get participants for an incident.
    """
    return IncidentService.get_participants(db, current_user.company_id, incident_id)

@router.post("/{incident_id}/evidence", response_model=schemas.IncidentEvidenceResponse)
def add_evidence(
    incident_id: str,
    payload: schemas.IncidentEvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Add evidence (photo, document link) to an incident.
    """
    return IncidentService.add_evidence(db, current_user.company_id, incident_id, current_user.id, payload)

@router.get("/{incident_id}/evidence", response_model=List[schemas.IncidentEvidenceResponse])
def get_evidence(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Get evidence for an incident.
    """
    return IncidentService.get_evidence(db, current_user.company_id, incident_id)
