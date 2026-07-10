from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user
from app.services.attendance_service import AttendanceService
from app.modules.attendance.services.attendance_workspace_service import AttendanceWorkspaceService
from app.modules.attendance.schemas.attendance_workspace_dto import AttendancePageResponse

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

@router.get("/worker/{worker_id}", response_model=AttendancePageResponse)
def get_worker_attendance(
    worker_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return AttendanceWorkspaceService.get_worker_history(db, current_user, worker_id, skip, limit)

@router.get("/site/{site_id}", response_model=AttendancePageResponse)
def get_site_attendance(
    site_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return AttendanceWorkspaceService.get_site_history(db, current_user, site_id, skip, limit)

@router.get("/contractor/{contractor_id}", response_model=AttendancePageResponse)
def get_contractor_attendance(
    contractor_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return AttendanceWorkspaceService.get_contractor_history(db, current_user, contractor_id, skip, limit)

@router.get("/department/{department_id}", response_model=AttendancePageResponse)
def get_department_attendance(
    department_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return AttendanceWorkspaceService.get_department_history(db, current_user, department_id, skip, limit)
