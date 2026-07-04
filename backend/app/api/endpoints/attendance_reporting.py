from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io

from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole, AttendanceStatus
from app.api.deps import get_current_user, PermissionChecker
from app.services.attendance_reporting_service import AttendanceReportingService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, query: schemas.AttendanceReportQuery) -> schemas.AttendanceReportQuery:
    """
    Enforces authorization isolation based on the user's role.
    """
    if current_user.role == UserRole.WORKER:
        # Workers can only see themselves
        query.worker_id = current_user.id
        query.company_id = current_user.company_id
    elif current_user.role == UserRole.SITE_MANAGER:
        # Site managers are locked to their company (site isolation handled at query time or explicitly here)
        query.company_id = current_user.company_id
        # Note: If site_id is passed, it should be validated against their managed sites. 
        # For foundation, locking to company is base.
    else:
        # Company Admins and above
        if current_user.company_id:
            query.company_id = current_user.company_id
            
    return query

@router.post("/reports", response_model=schemas.AttendanceReportResponse)
def get_attendance_report(
    query: schemas.AttendanceReportQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Paginated, filtered attendance reporting endpoint.
    """
    query = _enforce_tenant_isolation(current_user, query)
    return AttendanceReportingService.get_report(db, query)

@router.get("/reports/live", response_model=schemas.AttendanceReportResponse)
def get_live_attendance(
    site_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Convenience endpoint for live attendance (active check-ins).
    """
    query = schemas.AttendanceReportQuery(
        status=AttendanceStatus.CHECKED_IN.value,
        site_id=site_id,
        skip=skip,
        limit=limit
    )
    query = _enforce_tenant_isolation(current_user, query)
    return AttendanceReportingService.get_report(db, query)

@router.get("/me/today", response_model=schemas.AttendanceReportResponse)
def get_my_today_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Convenience endpoint for the logged-in worker's current day attendance.
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    query = schemas.AttendanceReportQuery(
        worker_id=current_user.id,
        start_date=today_start,
        skip=0,
        limit=50
    )
    return AttendanceReportingService.get_report(db, query)

@router.post("/export/csv")
def export_attendance_csv(
    query: schemas.AttendanceReportQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Streams attendance history as a CSV file.
    """
    query = _enforce_tenant_isolation(current_user, query)
    
    def iter_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        # Header
        writer.writerow(["ID", "Worker Name", "Site Name", "Check In", "Check Out", "Status", "Check In Method", "Check Out Method", "Correction Count", "Has Corrections"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        
        # Data streaming
        for row in AttendanceReportingService.get_export_generator(db, query):
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
            
    response = StreamingResponse(iter_csv(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=attendance_export.csv"
    return response
