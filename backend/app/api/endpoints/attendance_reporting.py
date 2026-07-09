from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io

from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, AttendanceStatus
from app.api.deps import get_current_user, PermissionChecker
from app.services.attendance_reporting_service import AttendanceReportingService

router = APIRouter()

@router.post("/reports", response_model=schemas.AttendanceReportResponse)
def get_attendance_report(
    query: schemas.AttendanceReportQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Paginated, filtered attendance reporting endpoint.
    """
    return AttendanceReportingService.get_report(db, query, current_user)

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
    return AttendanceReportingService.get_report(db, query, current_user)

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
    return AttendanceReportingService.get_report(db, query, current_user)

@router.post("/export/csv")
def export_attendance_csv(
    query: schemas.AttendanceReportQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Streams attendance history as a CSV file.
    """
    def iter_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        # Header
        writer.writerow([
            "Attendance ID", "Worker Name", "Site Name", 
            "Check-In Time", "Check-Out Time", "Status",
            "Check-In Method", "Check-Out Method",
            "Correction Count", "Has Corrections"
        ])
        yield output.getvalue()
        output.truncate(0)
        output.seek(0)
        
        for row in AttendanceReportingService.get_export_generator(db, query, current_user):
            writer.writerow(row)
            yield output.getvalue()
            output.truncate(0)
            output.seek(0)

    filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }

    return StreamingResponse(
        iter_csv(), 
        media_type="text/csv", 
        headers=headers
    )
