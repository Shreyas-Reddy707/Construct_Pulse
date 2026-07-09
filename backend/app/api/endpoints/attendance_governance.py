from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user, PermissionChecker
from app.services.attendance_governance_service import AttendanceGovernanceService

router = APIRouter()

@router.post("/{attendance_id}/admin-checkout", response_model=schemas.GovernanceResult)
def admin_checkout(
    attendance_id: str,
    request: schemas.AdminCheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.manage"))
):
    return AttendanceGovernanceService.administrative_checkout(
        session=db,
        attendance_id=attendance_id,
        performed_by=current_user,
        reason_code=request.reason_code,
        reason_notes=request.reason_notes
    )

@router.post("/{attendance_id}/correct", response_model=schemas.GovernanceResult)
def correct_attendance(
    attendance_id: str,
    request: schemas.AttendanceCorrectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.manage"))
):
    return AttendanceGovernanceService.correct_attendance(
        session=db,
        attendance_id=attendance_id,
        performed_by=current_user,
        reason_code=request.reason_code,
        reason_notes=request.reason_notes,
        new_check_in_time=request.check_in_time,
        new_check_out_time=request.check_out_time
    )

@router.get("/{attendance_id}/corrections", response_model=List[schemas.AttendanceCorrectionLogResponse])
def get_correction_history(
    attendance_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    return AttendanceGovernanceService.correction_history(
        session=db,
        attendance_id=attendance_id,
        performed_by=current_user
    )
