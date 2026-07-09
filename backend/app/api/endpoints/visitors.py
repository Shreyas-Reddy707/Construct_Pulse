from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User, UserRole
from app.schemas import schemas
from app.services.visitor_service import VisitorService

router = APIRouter()

@router.post("/register", response_model=schemas.VisitorVisitResponse)
def register_visit(
    payload: schemas.VisitorVisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registers a new visitor visit.
    """
    return VisitorService.register_visit(db, current_user.company_id, current_user.id, payload)

@router.post("/visits/{visit_id}/approve", response_model=schemas.VisitorVisitResponse)
def approve_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Approves a visitor visit request.
    """
    return VisitorService.approve_visit(db, current_user.company_id, visit_id, current_user.id)

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
    return VisitorService.deny_visit(db, current_user.company_id, visit_id, current_user.id, payload.reason)

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
    return VisitorService.cancel_visit(db, current_user.company_id, visit_id, current_user.id, payload.reason)

@router.post("/visits/{visit_id}/check-in", response_model=schemas.VisitorVisitResponse)
def check_in_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Records visitor arrival and check-in.
    """
    return VisitorService.check_in(db, current_user.company_id, visit_id, current_user.id)

@router.post("/visits/{visit_id}/check-out", response_model=schemas.VisitorVisitResponse)
def check_out_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Records visitor departure and check-out.
    """
    return VisitorService.check_out(db, current_user.company_id, visit_id, current_user.id)

@router.post("/visits/{visit_id}/expire", response_model=schemas.VisitorVisitResponse)
def expire_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.manage"))
):
    """
    Marks a visit as EXPIRED.
    """
    return VisitorService.expire_visit(db, current_user.company_id, visit_id, current_user.id)

@router.get("/dashboard", response_model=schemas.VisitorDashboard)
def get_dashboard(
    site_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("safety.view"))
):
    """
    Returns dashboard statistics for visitor management.
    """
    return VisitorService.get_dashboard(db, current_user.company_id, site_id)

@router.get("/visits", response_model=List[schemas.VisitorVisitResponse])
def list_visits(
    site_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists visitor visits with optional filtering.
    """
    return VisitorService.list_visits(db, current_user.company_id, site_id, status, skip, limit)
