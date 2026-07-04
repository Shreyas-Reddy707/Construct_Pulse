from typing import List, Generator, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, asc, desc

from app.models.models import Attendance, User, Site, AttendanceCorrectionLog
import uuid
from app.schemas.schemas import AttendanceReportQuery, AttendanceReportRow, AttendanceReportResponse, ReportMetadata

class AttendanceReportingService:
    ALLOWED_SORT_FIELDS = ["check_in_time", "check_out_time", "status"]

    @classmethod
    def _build_query(cls, session: Session, query_params: AttendanceReportQuery):
        # We need correction count, so we'll use an outer join with a subquery
        correction_subq = session.query(
            AttendanceCorrectionLog.attendance_id,
            func.count(AttendanceCorrectionLog.id).label('correction_count')
        ).group_by(AttendanceCorrectionLog.attendance_id).subquery()

        query = session.query(
            Attendance,
            User.name.label("worker_name"),
            Site.name.label("site_name"),
            func.coalesce(correction_subq.c.correction_count, 0).label('correction_count')
        ).join(
            User, Attendance.user_id == User.id, isouter=True
        ).join(
            Site, Attendance.site_id == Site.id, isouter=True
        ).outerjoin(
            correction_subq, Attendance.id == correction_subq.c.attendance_id
        )

        # Filters
        if query_params.start_date:
            query = query.filter(Attendance.check_in_time >= query_params.start_date)
        if query_params.end_date:
            query = query.filter(Attendance.check_in_time <= query_params.end_date)
        if query_params.worker_id:
            query = query.filter(Attendance.user_id == query_params.worker_id)
        if query_params.site_id:
            query = query.filter(Attendance.site_id == query_params.site_id)
        if query_params.company_id:
            query = query.filter(Attendance.company_id == query_params.company_id)
        if query_params.status:
            query = query.filter(Attendance.status == query_params.status)

        # Sorting (Whitelist)
        sort_field = query_params.sort_by if query_params.sort_by in cls.ALLOWED_SORT_FIELDS else "check_in_time"
        sort_column = getattr(Attendance, sort_field)
        
        if query_params.sort_order and query_params.sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        return query

    @classmethod
    def _map_to_dto(cls, row) -> AttendanceReportRow:
        attendance, worker_name, site_name, correction_count = row
        return AttendanceReportRow(
            attendance_id=attendance.id,
            worker_id=attendance.user_id,
            worker_name=worker_name,
            site_id=attendance.site_id,
            site_name=site_name,
            company_id=attendance.company_id,
            check_in_time=attendance.check_in_time,
            check_out_time=attendance.check_out_time,
            status=attendance.status.value,
            check_in_method=attendance.check_in_method.value if attendance.check_in_method else None,
            check_out_method=attendance.check_out_method.value if attendance.check_out_method else None,
            correction_count=correction_count,
            has_corrections=correction_count > 0
        )

    @classmethod
    def get_report(
        cls, 
        session: Session, 
        query_params: AttendanceReportQuery
    ) -> AttendanceReportResponse:
        """
        Executes a paginated reporting query and returns a standardized response.
        """
        query = cls._build_query(session, query_params)
        
        # Count total records matching filters (before pagination)
        total_records = query.count()
        
        # Pagination
        query = query.offset(query_params.skip).limit(query_params.limit)
        
        rows = [cls._map_to_dto(row) for row in query.all()]
        
        metadata = ReportMetadata(
            total_records=total_records,
            returned_records=len(rows),
            skip=query_params.skip,
            limit=query_params.limit,
            applied_filters={
                k: v for k, v in query_params.dict().items() 
                if v is not None and k not in ['skip', 'limit', 'sort_by', 'sort_order']
            }
        )
        
        return AttendanceReportResponse(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            metadata=metadata,
            rows=rows
        )

    @classmethod
    def get_export_generator(
        cls, 
        session: Session, 
        query_params: AttendanceReportQuery
    ) -> Generator[Tuple, None, None]:
        """
        Yields raw tuples for CSV streaming. Does not paginate.
        """
        # Remove pagination limits for export
        query = cls._build_query(session, query_params)
        
        # Stream results using yield_per to avoid loading everything into memory
        for row in query.yield_per(100):
            dto = cls._map_to_dto(row)
            yield (
                dto.attendance_id,
                dto.worker_name or "Unknown",
                dto.site_name or "Unknown",
                dto.check_in_time.isoformat() if dto.check_in_time else "",
                dto.check_out_time.isoformat() if dto.check_out_time else "",
                dto.status,
                dto.check_in_method or "",
                dto.check_out_method or "",
                dto.correction_count,
                "Yes" if dto.has_corrections else "No"
            )
