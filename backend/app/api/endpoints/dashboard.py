from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from app.db.database import get_db
from app.models.models import User, Company, Site, WorkerStatus, Attendance, AttendanceStatus
from app.api.deps import get_current_user, RoleChecker
from datetime import datetime, date, timedelta, timezone

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["Company Admin", "System Admin", "Site Manager"]))
):
    company_id = current_user.company_id
    if current_user.role.value == "System Admin":
        # System Admin sees all by default unless we pass a param
        pass

    users_query = db.query(User).filter(User.role == UserRole.WORKER)
    sites_query = db.query(Site)
    attendance_query = db.query(Attendance)
    
    if company_id:
        users_query = users_query.filter(User.company_id == company_id)
        sites_query = sites_query.filter(Site.company_id == company_id)
        attendance_query = attendance_query.join(User).filter(User.company_id == company_id)

    total_workers = users_query.count()
    pending_workers = users_query.filter(User.status == WorkerStatus.PENDING).count()
    approved_workers = users_query.filter(User.status == WorkerStatus.APPROVED).count()
    suspended_workers = users_query.filter(User.status == WorkerStatus.SUSPENDED).count()

    active_sites = sites_query.filter(Site.status == "active").count()

    today_utc = datetime.now(timezone.utc).date()
    yesterday_utc = datetime.now(timezone.utc) - timedelta(hours=24)

    checked_in_today = attendance_query.filter(
        cast(Attendance.check_in_time, Date) == today_utc
    ).count()
    
    checked_out_today = attendance_query.filter(
        cast(Attendance.check_out_time, Date) == today_utc
    ).count()
    
    # "Workers on site" must exclude stale records older than 24 hours
    workers_on_site = attendance_query.filter(
        Attendance.check_out_time == None,
        Attendance.status == AttendanceStatus.CHECKED_IN,
        Attendance.check_in_time >= yesterday_utc
    ).count()

    return {
        "total_workers": total_workers,
        "pending_workers": pending_workers,
        "approved_workers": approved_workers,
        "suspended_workers": suspended_workers,
        "checked_in_today": checked_in_today,
        "checked_out_today": checked_out_today,
        "active_sites": active_sites,
        "workers_on_site": workers_on_site
    }
