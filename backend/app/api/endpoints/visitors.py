from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.visitor_service import VisitorService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, resource_company_id: str):
    if current_user.role == UserRole.SYSTEM_ADMIN:
        return
    if not current_user.company_id or current_user.company_id != resource_company_id:
        raise HTTPException(status_code=403, detail="Tenant isolation violation")

@router.post("/register", response_model=schemas.VisitorVisitResponse)
def register_visit(
    payload: schemas.VisitorVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registers a new visitor visit.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return VisitorService.register_visit(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/approve", response_model=schemas.VisitorVisitResponse)
def approve_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Approves a visitor visit request.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.approve_visit(db, current_user.company_id, visit_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/deny", response_model=schemas.VisitorVisitResponse)
def deny_visit(
    visit_id: str,
    payload: schemas.VisitDeny,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Denies a visitor visit request.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.deny_visit(db, current_user.company_id, visit_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/cancel", response_model=schemas.VisitorVisitResponse)
def cancel_visit(
    visit_id: str,
    payload: schemas.VisitCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Cancels an existing visit request.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.cancel_visit(db, current_user.company_id, visit_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/check-in", response_model=schemas.VisitorVisitResponse)
def check_in_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Records visitor arrival and check-in.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.check_in(db, current_user.company_id, visit_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/check-out", response_model=schemas.VisitorVisitResponse)
def check_out_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Records visitor departure and check-out.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.check_out(db, current_user.company_id, visit_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/visits/{visit_id}/expire", response_model=schemas.VisitorVisitResponse)
def expire_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Expires a visit that was not checked-in within its validity period.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    try:
        return VisitorService.expire_visit(db, current_user.company_id, visit_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/visits", response_model=List[schemas.VisitorVisitResponse])
def list_visits(
    site_id: Optional[str] = None,
    host_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Lists visitor visits.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return VisitorService.list_visits(db, current_user.company_id, site_id, host_id, skip, limit)

@router.get("/visits/{visit_id}", response_model=schemas.VisitorVisitResponse)
def get_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Gets details of a specific visit.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    visit = VisitorService.get_visit(db, current_user.company_id, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.get("/dashboard", response_model=schemas.VisitorDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Gets dashboard summary of visits.
    """
    _enforce_tenant_isolation(current_user, current_user.company_id)
    return VisitorService.dashboard(db, current_user.company_id)
