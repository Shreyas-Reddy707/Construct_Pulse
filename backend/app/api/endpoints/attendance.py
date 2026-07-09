from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user
from app.services.attendance_service import AttendanceService

router = APIRouter()

@router.post("/check-in", response_model=schemas.AttendanceResponse)
def check_in(checkin_data: schemas.AttendanceCheckIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AttendanceService.check_in(
        session=db,
        user=current_user,
        qr_token=checkin_data.qr_token,
        gps_latitude=checkin_data.gps_latitude,
        gps_longitude=checkin_data.gps_longitude
    )

@router.post("/check-out", response_model=schemas.AttendanceResponse)
def check_out(checkout_data: schemas.AttendanceCheckOut, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AttendanceService.check_out(
        session=db,
        user=current_user,
        site_id=checkout_data.site_id
    )
