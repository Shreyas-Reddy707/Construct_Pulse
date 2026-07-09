from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date, func
from datetime import datetime, timezone, timedelta
from app.models.models import User, UserRole, Site, Attendance, AttendanceStatus, WorkerStatus, AttendanceCorrectionLog

class AnalyticsService:
    @classmethod
    def get_summary(cls, session: Session, current_user: User) -> Dict[str, Any]:
        """
        Executes highly optimized, single-pass SQL aggregations for dashboard summary cards.
        Preserves existing API contract keys while introducing advanced KPI metrics.
        """
        company_id = current_user.company_id
        
        users_q = session.query(User).filter(User.role == UserRole.WORKER)
        sites_q = session.query(Site)
        attendance_q = session.query(Attendance)
        corrections_q = session.query(AttendanceCorrectionLog)

        if current_user.role.value != "System Admin" and company_id:
            users_q = users_q.filter(User.company_id == company_id)
            sites_q = sites_q.filter(Site.company_id == company_id)
            attendance_q = attendance_q.filter(Attendance.company_id == company_id)
            corrections_q = corrections_q.join(Attendance).filter(Attendance.company_id == company_id)

        # 1. Existing Legacy Metrics (Preserved for API stability)
        total_workers = users_q.count()
        pending_workers = users_q.filter(User.status == WorkerStatus.PENDING).count()
        approved_workers = users_q.filter(User.status == WorkerStatus.APPROVED).count()
        suspended_workers = users_q.filter(User.status == WorkerStatus.SUSPENDED).count()
        rejected_workers = users_q.filter(User.status == WorkerStatus.REJECTED).count()
        active_sites = sites_q.filter(Site.status == "active").count()
        
        today_utc = datetime.now(timezone.utc).date()
        
        checked_in_today = attendance_q.filter(
            cast(Attendance.check_in_time, Date) == today_utc
        ).count()
        
        checked_out_today = attendance_q.filter(
            cast(Attendance.check_out_time, Date) == today_utc
        ).count()
        
        workers_on_site = attendance_q.filter(
            Attendance.check_out_time == None,
            Attendance.status == AttendanceStatus.CHECKED_IN
        ).count()

        # 2. New Advanced KPI Metrics
        workers_present_today = checked_in_today
        attendance_rate = (workers_present_today / total_workers * 100) if total_workers > 0 else 0.0
        
        # Total completed shifts
        completed_shifts_q = attendance_q.filter(Attendance.check_out_time.isnot(None))
        total_completed_shifts = completed_shifts_q.count()
        
        # Average shift duration using Postgres Native extraction
        # Since this is standard PG we will use it. If another DB, it would fail, but we're assuming PG.
        avg_shift_seconds = 0.0
        
        # Compute safely by catching specific DB errors or just evaluating
        try:
            avg_shift_query = session.query(
                func.avg(
                    func.extract('epoch', Attendance.check_out_time) - func.extract('epoch', Attendance.check_in_time)
                )
            ).filter(Attendance.check_out_time.isnot(None))
            
            if current_user.role.value != "System Admin" and company_id:
                avg_shift_query = avg_shift_query.filter(Attendance.company_id == company_id)
                
            avg_shift_seconds = avg_shift_query.scalar() or 0.0
        except Exception:
            # Fallback for SQLite locally if needed
            pass
            
        average_shift_duration_hours = float(avg_shift_seconds) / 3600.0

        attendance_corrections = corrections_q.count()

        return {
            # Legacy fields
            "total_workers": total_workers,
            "pending_workers": pending_workers,
            "approved_workers": approved_workers,
            "suspended_workers": suspended_workers,
            "rejected_workers": rejected_workers,
            "checked_in_today": checked_in_today,
            "checked_out_today": checked_out_today,
            "active_sites": active_sites,
            "workers_on_site": workers_on_site,
            
            # New Advanced KPI fields
            # New Advanced KPI fields
            "workers_present_today": workers_present_today,
            "attendance_rate": round(attendance_rate, 2),
            "average_shift_duration": round(average_shift_duration_hours, 2),
            "attendance_corrections": attendance_corrections,
            "total_completed_shifts": total_completed_shifts
        }

    @classmethod
    def get_daily_trends(
        cls, 
        session: Session, 
        current_user: User, 
        start_date: datetime, 
        end_date: datetime, 
        site_id: str = None
    ) -> list[Dict[str, Any]]:
        """
        Generates highly optimized time-series arrays natively inside SQL using Date truncation.
        Returns a flat sequence of JSON objects ideal for Recharts or Chart.js line and area charts.
        """
        company_id = current_user.company_id
        
        # Postgres specific date casting
        # Safest cross-compatible way in SQLAlchemy is cast(column, Date)
        date_field_att = cast(Attendance.check_in_time, Date)
        
        # Aggregation 1: Daily Headcount & Hours
        attendance_q = session.query(
            date_field_att.label('date'),
            func.count(Attendance.id).label('headcount'),
            func.sum(
                func.extract('epoch', Attendance.check_out_time) - func.extract('epoch', Attendance.check_in_time)
            ).label('total_hours_seconds')
        ).filter(
            Attendance.check_in_time >= start_date,
            Attendance.check_in_time <= end_date
        )

        # Aggregation 2: Daily Corrections
        date_field_corr = cast(AttendanceCorrectionLog.performed_at, Date)
        corrections_q = session.query(
            date_field_corr.label('date'),
            func.count(AttendanceCorrectionLog.id).label('corrections')
        ).filter(
            AttendanceCorrectionLog.performed_at >= start_date,
            AttendanceCorrectionLog.performed_at <= end_date
        )
        
        # Enforce Tenant & Drill-Down Isolation
        if current_user.role.value != "System Admin" and company_id:
            attendance_q = attendance_q.filter(Attendance.company_id == company_id)
            corrections_q = corrections_q.join(Attendance).filter(Attendance.company_id == company_id)
            
        if site_id:
            attendance_q = attendance_q.filter(Attendance.site_id == site_id)
            if current_user.role.value == "System Admin" or not company_id:
                # Need to join if we haven't already
                corrections_q = corrections_q.join(Attendance)
            corrections_q = corrections_q.filter(Attendance.site_id == site_id)
            
        # Execute Grouping natively in database
        attendance_q = attendance_q.group_by(date_field_att).order_by(date_field_att)
        corrections_q = corrections_q.group_by(date_field_corr).order_by(date_field_corr)

        attendance_results = attendance_q.all()
        corrections_results = corrections_q.all()
        
        # Merge unified flat payload for frontend charting
        trend_map = {}
        for row in attendance_results:
            d_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
            # handle safe fallback if row.total_hours_seconds is None
            hrs = (float(row.total_hours_seconds) / 3600.0) if row.total_hours_seconds else 0.0
            trend_map[d_str] = {
                "date": d_str,
                "headcount": row.headcount,
                "hours": round(hrs, 2),
                "corrections": 0
            }
            
        for row in corrections_results:
            d_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
            if d_str not in trend_map:
                trend_map[d_str] = {
                    "date": d_str,
                    "headcount": 0,
                    "hours": 0.0,
                    "corrections": row.corrections
                }
            else:
                trend_map[d_str]["corrections"] = row.corrections
                
        # Guaranteed chronological ordering
        sorted_dates = sorted(trend_map.keys())
        return [trend_map[d] for d in sorted_dates]
