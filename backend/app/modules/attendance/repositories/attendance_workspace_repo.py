from sqlalchemy.orm import Session
from sqlalchemy import literal, select, union_all, func, desc, asc
from typing import Tuple, List, Any
from app.models.models import Attendance, Site, User

class AttendanceWorkspaceRepository:
    @classmethod
    def _execute_attendance_workspace_query(
        cls, 
        session: Session, 
        base_query: Any, 
        skip: int, 
        limit: int
    ) -> Tuple[List[Tuple[str, str, str, str, str, str]], int]:
        """
        Internal private helper.
        Executes the split-count and the UNION ALL query for pagination.
        base_query: A SQLAlchemy Query object with filters and Site join already applied.
        """
        # 1. Execute single-roundtrip split-count
        count_result = base_query.with_entities(
            func.count(Attendance.id).label("total_shifts"),
            func.count(Attendance.check_out_time).label("completed_shifts")
        ).first()
        
        total_events = (count_result.total_shifts or 0) + (count_result.completed_shifts or 0)
        
        # 2. Build UNION ALL CTE using the exact base query filters
        check_in_query = base_query.with_entities(
            Attendance.id,
            Attendance.user_id,
            Attendance.site_id,
            Site.name.label("site_name"),
            literal("check_in").label("scan_type"),
            Attendance.check_in_time.label("timestamp")
        )
        
        check_out_query = base_query.filter(
            Attendance.check_out_time.is_not(None)
        ).with_entities(
            Attendance.id,
            Attendance.user_id,
            Attendance.site_id,
            Site.name.label("site_name"),
            literal("check_out").label("scan_type"),
            Attendance.check_out_time.label("timestamp")
        )
        
        union_query = check_in_query.union_all(check_out_query)
        
        # Apply deterministic ordering and pagination
        # We wrap the union in a subquery to sort and paginate it securely
        subq = union_query.subquery()
        
        final_query = session.query(
            subq.c.id,
            subq.c.user_id,
            subq.c.site_id,
            subq.c.site_name,
            subq.c.scan_type,
            subq.c.timestamp
        ).order_by(
            desc(subq.c.timestamp),
            asc(subq.c.id),
            asc(subq.c.scan_type)
        ).offset(skip).limit(limit)
        
        rows = final_query.all()
        return rows, total_events

    @classmethod
    def get_worker_history(cls, session: Session, company_id: str, worker_id: str, skip: int, limit: int):
        base_query = session.query(Attendance).join(
            Site, Attendance.site_id == Site.id
        ).filter(
            Attendance.company_id == company_id,
            Attendance.user_id == worker_id
        )
        return cls._execute_attendance_workspace_query(session, base_query, skip, limit)
        
    @classmethod
    def get_site_history(cls, session: Session, company_id: str, site_id: str, skip: int, limit: int):
        base_query = session.query(Attendance).join(
            Site, Attendance.site_id == Site.id
        ).filter(
            Attendance.company_id == company_id,
            Attendance.site_id == site_id
        )
        return cls._execute_attendance_workspace_query(session, base_query, skip, limit)
        
    @classmethod
    def get_contractor_history(cls, session: Session, company_id: str, contractor_id: str, skip: int, limit: int):
        base_query = session.query(Attendance).join(
            Site, Attendance.site_id == Site.id
        ).join(
            User, Attendance.user_id == User.id
        ).filter(
            Attendance.company_id == company_id,
            User.contractor_id == contractor_id
        )
        return cls._execute_attendance_workspace_query(session, base_query, skip, limit)

    @classmethod
    def get_department_history(cls, session: Session, company_id: str, department_id: str, skip: int, limit: int):
        base_query = session.query(Attendance).join(
            Site, Attendance.site_id == Site.id
        ).join(
            User, Attendance.user_id == User.id
        ).filter(
            Attendance.company_id == company_id,
            User.department_id == department_id
        )
        return cls._execute_attendance_workspace_query(session, base_query, skip, limit)
