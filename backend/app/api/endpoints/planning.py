from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.workforce_plan_service import WorkforcePlanService

router = APIRouter()

@router.post("", response_model=schemas.WorkforcePlanResponse)
def create_plan_draft(
    payload: schemas.WorkforcePlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.manage"))
):
    """
    Creates a new workforce plan draft.
    """
    return WorkforcePlanService.create_draft(db, current_user.company_id, current_user.id, payload)

@router.post("/{plan_id}/departments", response_model=schemas.WorkforcePlanResponse)
def set_department_targets(
    plan_id: str,
    targets: List[schemas.DepartmentTargetCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.manage"))
):
    """
    Sets department targets for a draft workforce plan.
    """
    return WorkforcePlanService.set_department_targets(db, current_user.company_id, plan_id, current_user.id, targets)

@router.post("/{plan_id}/contractors", response_model=schemas.WorkforcePlanResponse)
def set_contractor_targets(
    plan_id: str,
    targets: List[schemas.ContractorTargetCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.manage"))
):
    """
    Sets contractor targets for a draft workforce plan.
    """
    return WorkforcePlanService.set_contractor_targets(db, current_user.company_id, plan_id, current_user.id, targets)

@router.post("/{plan_id}/approve", response_model=schemas.WorkforcePlanResponse)
def approve_plan(
    plan_id: str,
    payload: schemas.ApprovePlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.approve"))
):
    """
    Approves a workforce plan.
    """
    return WorkforcePlanService.approve(db, current_user.company_id, plan_id, current_user.id, payload.reason)

@router.post("/{plan_id}/archive", response_model=schemas.WorkforcePlanResponse)
def archive_plan(
    plan_id: str,
    payload: schemas.ArchivePlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.manage"))
):
    """
    Archives a workforce plan.
    """
    return WorkforcePlanService.archive(db, current_user.company_id, plan_id, current_user.id, payload.reason)

@router.get("", response_model=List[schemas.WorkforcePlanResponse])
def list_plans(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists workforce plans.
    """
    return WorkforcePlanService.list_plans(db, current_user.company_id, site_id, skip, limit)

@router.get("/dashboard", response_model=schemas.PlanningDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("planning.manage"))
):
    """
    Gets dashboard summary of workforce plans.
    """
    return WorkforcePlanService.dashboard(db, current_user.company_id)

@router.get("/{plan_id}", response_model=schemas.WorkforcePlanResponse)
def get_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets details of a specific workforce plan.
    """
    return WorkforcePlanService.get_plan(db, current_user.company_id, plan_id)
