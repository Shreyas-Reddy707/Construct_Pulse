from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.incident_service import IncidentService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, resource_company_id: str):
    if current_user.role == UserRole.SYSTEM_ADMIN:
        return
    if not current_user.company_id or current_user.company_id != resource_company_id:
        raise HTTPException(status_code=403, detail="Tenant isolation violation")

@router.post("", response_model=schemas.IncidentResponse)
def create_incident(
    payload: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new incident report. Workers and above can create incidents.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return IncidentService.create_incident(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return IncidentService.list_incidents(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.IncidentDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Returns incident operational counts.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return IncidentService.dashboard(db, current_user.company_id)

@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    _enforce_tenant_isolation(current_user, current_user.company_id)
    incident = IncidentService.get_incident(db, current_user.company_id, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

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
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.assign_investigator(db, current_user.company_id, incident_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.update_status(db, current_user.company_id, incident_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{incident_id}/participants", response_model=schemas.IncidentParticipantResponse)
def add_participant(
    incident_id: str,
    payload: schemas.IncidentParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Add a participant to the incident.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.add_participant(db, current_user.company_id, incident_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{incident_id}/participants", response_model=List[schemas.IncidentParticipantResponse])
def get_participants(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.get_participants(db, current_user.company_id, incident_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{incident_id}/evidence", response_model=schemas.IncidentEvidenceResponse)
def add_evidence(
    incident_id: str,
    payload: schemas.IncidentEvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Add an evidence record to the incident.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.add_evidence(db, current_user.company_id, incident_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{incident_id}/evidence", response_model=List[schemas.IncidentEvidenceResponse])
def get_evidence(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return IncidentService.get_evidence(db, current_user.company_id, incident_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
