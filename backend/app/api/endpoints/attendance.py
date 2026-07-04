from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole, Attendance, Site
from app.api.deps import get_current_user, RoleChecker, PermissionChecker
from app.services.attendance_service import AttendanceService

router = APIRouter()

@router.post("/check-in", response_model=schemas.AttendanceResponse)
def check_in(checkin_data: schemas.AttendanceCheckIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        attendance = AttendanceService.check_in(
            session=db,
            user=current_user,
            qr_token=checkin_data.qr_token,
            gps_latitude=checkin_data.gps_latitude,
            gps_longitude=checkin_data.gps_longitude
        )
        return attendance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/check-out", response_model=schemas.AttendanceResponse)
def check_out(checkout_data: schemas.AttendanceCheckOut, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        attendance = AttendanceService.check_out(
            session=db,
            user=current_user,
            site_id=checkout_data.site_id
        )
        return attendance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


