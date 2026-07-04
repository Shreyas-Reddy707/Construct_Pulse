from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.payroll_service import PayrollService

router = APIRouter()

@router.post("/run", response_model=schemas.PayrollRunResponse)
def create_payroll_run(
    payload: schemas.PayrollRunCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Initiates a new draft payroll run. Requires 'payroll.manage' permission.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return PayrollService.create_payroll_run(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{payroll_run_id}/generate", response_model=schemas.PayrollRunResponse)
def generate_payroll(
    payroll_run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Generates payroll snapshots for a DRAFT run based on certified read models.
    """
    try:
        return PayrollService.generate_payroll(db, payroll_run_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/employee/{payroll_employee_id}/adjustments", response_model=schemas.PayrollEmployeeResponse)
def add_adjustment(
    payroll_employee_id: str,
    payload: schemas.PayrollAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Adds a manual adjustment to a payroll snapshot. Allowed only in DRAFT status.
    """
    try:
        return PayrollService.add_adjustment(db, payroll_employee_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{payroll_run_id}/approve", response_model=schemas.PayrollRunResponse)
def approve_payroll(
    payroll_run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.approve"))
):
    """
    Approves a payroll run. Requires 'payroll.approve' permission.
    """
    try:
        return PayrollService.approve(db, payroll_run_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{payroll_run_id}/lock", response_model=schemas.PayrollRunResponse)
def lock_payroll(
    payroll_run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.approve"))
):
    """
    Permanently locks an APPROVED payroll run.
    """
    try:
        return PayrollService.lock(db, payroll_run_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.PayrollRunResponse])
def list_payroll_runs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Lists payroll runs for the current user's company.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    return PayrollService.list_payroll_runs(db, current_user.company_id, skip, limit)

@router.get("/dashboard", response_model=schemas.PayrollDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Gets dashboard summary of payroll runs.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    return PayrollService.dashboard(db, current_user.company_id)

@router.get("/{payroll_run_id}", response_model=schemas.PayrollRunResponse)
def get_payroll_run(
    payroll_run_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("payroll.manage"))
):
    """
    Gets details of a specific payroll run.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    
    payroll_run = PayrollService.get_payroll_run(db, payroll_run_id, current_user.company_id)
    if not payroll_run:
        raise HTTPException(status_code=404, detail="Payroll run not found")
    return payroll_run
