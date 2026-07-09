from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.safety_operations_service import SafetyOperationsService

router = APIRouter()

@router.post("/observations", response_model=schemas.SafetyObservationResponse)
def create_observation(
    payload: schemas.SafetyObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new safety observation.
    """
    return SafetyOperationsService.create_observation(db, current_user.company_id, current_user.id, payload)

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
    return SafetyOperationsService.assign_corrective_action(db, current_user.company_id, observation_id, current_user.id, payload)

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
    return SafetyOperationsService.update_observation_status(db, current_user.company_id, observation_id, current_user.id, payload.status, payload.reason)

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
    return SafetyOperationsService.update_corrective_action_status(db, current_user.company_id, action_id, current_user.id, payload.status, payload.reason)

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
    return SafetyOperationsService.verify_observation(db, current_user.company_id, observation_id, current_user.id, payload.reason)

@router.post("/observations/{observation_id}/close", response_model=schemas.SafetyObservationResponse)
def close_observation(
    observation_id: str,
    payload: schemas.ObservationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Closes a verified observation.
    """
    return SafetyOperationsService.close_observation(db, current_user.company_id, observation_id, current_user.id, payload.reason)

@router.get("/observations", response_model=List[schemas.SafetyObservationResponse])
def list_observations(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Lists safety observations within the tenant.
    """
    return SafetyOperationsService.list_observations(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.SafetyDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Returns safety observation statistics.
    """
    return SafetyOperationsService.dashboard(db, current_user.company_id)

@router.get("/observations/{observation_id}", response_model=schemas.SafetyObservationResponse)
def get_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Gets details of a specific safety observation.
    """
    return SafetyOperationsService.get_observation(db, current_user.company_id, observation_id)
