from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.emergency_muster_service import EmergencyMusterService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, resource_company_id: str):
    if current_user.role == UserRole.SYSTEM_ADMIN:
        return
    if not current_user.company_id or current_user.company_id != resource_company_id:
        raise HTTPException(status_code=403, detail="Tenant isolation violation")

@router.post("/start", response_model=schemas.MusterSessionResponse)
def start_muster_session(
    payload: schemas.MusterSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view")) # Using attendance.view as placeholder for now, assuming site managers have it
):
    """
    Starts an emergency muster session for a site.
    Captures the occupancy snapshot and generates participants.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return EmergencyMusterService.create_session(db, current_user.company_id, current_user.id, payload)

@router.get("/active/{site_id}", response_model=List[schemas.MusterSessionResponse])
def get_active_sessions(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Lists active muster sessions for a site.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return EmergencyMusterService.list_active_sessions(db, current_user.company_id, site_id)

@router.get("/{session_id}", response_model=schemas.MusterSessionResponse)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    session = EmergencyMusterService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Muster session not found")
    _enforce_tenant_isolation(current_user, session.company_id)
    return session

@router.get("/{session_id}/dashboard", response_model=schemas.MusterDashboard)
def get_dashboard(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    session = EmergencyMusterService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Muster session not found")
    _enforce_tenant_isolation(current_user, session.company_id)
    return EmergencyMusterService.dashboard(db, session_id)

@router.get("/{session_id}/participants", response_model=List[schemas.MusterParticipantResponse])
def get_participants(
    session_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    session = EmergencyMusterService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Muster session not found")
    _enforce_tenant_isolation(current_user, session.company_id)
    return EmergencyMusterService.get_participants(db, session_id, skip, limit)

@router.post("/participants/{participant_id}/acknowledge", response_model=schemas.MusterParticipantResponse)
def acknowledge_participant(
    participant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Worker self-acknowledgement or direct acknowledgement.
    """
    return EmergencyMusterService.acknowledge_participant(db, participant_id, current_user.id)

@router.post("/participants/{participant_id}/override", response_model=schemas.MusterParticipantResponse)
def override_participant_status(
    participant_id: str,
    payload: schemas.MusterOverrideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Manager manual override for a participant's safety status.
    """
    return EmergencyMusterService.manager_override(db, participant_id, current_user.id, payload)

@router.post("/{session_id}/complete", response_model=schemas.MusterSessionResponse)
def complete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    session = EmergencyMusterService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Muster session not found")
    _enforce_tenant_isolation(current_user, session.company_id)
    return EmergencyMusterService.complete_session(db, session_id, current_user.id)

@router.post("/{session_id}/cancel", response_model=schemas.MusterSessionResponse)
def cancel_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    session = EmergencyMusterService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Muster session not found")
    _enforce_tenant_isolation(current_user, session.company_id)
    return EmergencyMusterService.cancel_session(db, session_id, current_user.id)
