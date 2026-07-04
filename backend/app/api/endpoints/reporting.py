from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.models import User
from app.schemas.schemas import (
    ReportGenerateRequest, ComplianceReportResponse, ReportDashboard
)
from app.services.reporting_service import ReportingService

router = APIRouter()

@router.post("/generate", response_model=ComplianceReportResponse)
def generate_report(
    payload: ReportGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a new compliance report snapshot.
    Orchestrates data from certified downstream foundations.
    """
    # Assuming PermissionChecker enforces reporting.generate and validates company_id here
    try:
        report = ReportingService.generate_report(
            db=db,
            company_id=current_user.company_id,
            current_user_id=current_user.id,
            payload=payload
        )
        return report
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{report_id}/archive", response_model=ComplianceReportResponse)
def archive_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Archive a compliance report.
    This increments the report version and adds an audit log.
    """
    try:
        report = ReportingService.archive(
            db=db,
            report_id=report_id,
            current_user_id=current_user.id
        )
        return report
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ComplianceReportResponse])
def list_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List compliance reports for the user's tenant.
    """
    return ReportingService.list_reports(
        db=db,
        company_id=current_user.company_id,
        skip=skip,
        limit=limit
    )

@router.get("/dashboard", response_model=ReportDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the operational reporting dashboard (counters only).
    """
    return ReportingService.dashboard(
        db=db,
        company_id=current_user.company_id
    )

@router.get("/{report_id}", response_model=ComplianceReportResponse)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch a specific report, including its immutable snapshot data.
    """
    report = ReportingService.get_snapshot(
        db=db,
        report_id=report_id,
        company_id=current_user.company_id
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
