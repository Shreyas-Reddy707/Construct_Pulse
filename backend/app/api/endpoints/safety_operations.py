from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.safety_operations_service import SafetyOperationsService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, resource_company_id: str):
    if current_user.role == UserRole.SYSTEM_ADMIN:
        return
    if not current_user.company_id or current_user.company_id != resource_company_id:
        raise HTTPException(status_code=403, detail="Tenant isolation violation")

@router.post("/observations", response_model=schemas.SafetyObservationResponse)
def create_observation(
    payload: schemas.SafetyObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Anyone authenticated can report
):
    """
    Creates a new safety observation.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return SafetyOperationsService.create_observation(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/observations/{observation_id}/actions", response_model=schemas.SafetyObservationResponse)
def assign_action(
    observation_id: str,
    payload: schemas.CorrectiveActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Assigns a corrective action to an observation.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyOperationsService.assign_corrective_action(db, current_user.company_id, observation_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/observations/{observation_id}/status", response_model=schemas.SafetyObservationResponse)
def update_observation_status(
    observation_id: str,
    payload: schemas.ObservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Updates the status of an observation.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyOperationsService.update_observation_status(db, current_user.company_id, observation_id, current_user.id, payload.status, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/actions/{action_id}/status", response_model=schemas.SafetyObservationResponse)
def update_action_status(
    action_id: str,
    payload: schemas.CorrectiveActionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Updates the status of a corrective action.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyOperationsService.update_corrective_action_status(db, current_user.company_id, action_id, current_user.id, payload.status, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/observations/{observation_id}/verify", response_model=schemas.SafetyObservationResponse)
def verify_observation(
    observation_id: str,
    payload: schemas.ObservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Verifies an observation.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyOperationsService.verify_observation(db, current_user.company_id, observation_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/observations/{observation_id}/close", response_model=schemas.SafetyObservationResponse)
def close_observation(
    observation_id: str,
    payload: schemas.ObservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Closes an observation.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return SafetyOperationsService.close_observation(db, current_user.company_id, observation_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/observations", response_model=List[schemas.SafetyObservationResponse])
def list_observations(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Lists safety observations.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return SafetyOperationsService.list_observations(db, current_user.company_id, site_id, skip, limit)

@router.get("/observations/{observation_id}", response_model=schemas.SafetyObservationResponse)
def get_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Gets details of a specific safety observation.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    observation = SafetyOperationsService.get_observation(db, current_user.company_id, observation_id)
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    return observation

@router.get("/dashboard", response_model=schemas.SafetyDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Gets dashboard summary of safety operations.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return SafetyOperationsService.dashboard(db, current_user.company_id)
