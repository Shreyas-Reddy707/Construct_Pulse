from sqlalchemy.orm import Session
from app.models.models import User
from app.modules.attendance.repositories.attendance_workspace_repo import AttendanceWorkspaceRepository
from app.modules.attendance.schemas.attendance_workspace_dto import AttendanceLogResponse, AttendancePageResponse

class AttendanceWorkspaceService:
    @staticmethod
    def _map_to_page_response(rows, total_records: int, skip: int, limit: int) -> AttendancePageResponse:
        items = []
        for row in rows:
            # row: (id, user_id, site_id, site_name, scan_type, timestamp)
            att_id = row.id
            scan_type = row.scan_type
            
            # Synthesize deterministic ID to prevent React duplicate key crashes
            synthesized_id = f"{att_id}-in" if scan_type == "check_in" else f"{att_id}-out"
            
            # Format timestamp safely
            ts_str = row.timestamp.isoformat() if row.timestamp else ""
            
            items.append(AttendanceLogResponse(
                id=synthesized_id,
                attendance_id=att_id,
                worker_id=row.user_id,
                site_id=row.site_id,
                site_name=row.site_name,
                scan_type=scan_type,
                timestamp=ts_str
            ))
            
        return AttendancePageResponse(
            items=items,
            total_records=total_records,
            skip=skip,
            limit=limit
        )

    @classmethod
    def get_worker_history(cls, session: Session, current_user: User, worker_id: str, skip: int, limit: int) -> AttendancePageResponse:
        rows, total = AttendanceWorkspaceRepository.get_worker_history(
            session=session, 
            company_id=current_user.company_id, 
            worker_id=worker_id, 
            skip=skip, 
            limit=limit
        )
        return cls._map_to_page_response(rows, total, skip, limit)
        
    @classmethod
    def get_site_history(cls, session: Session, current_user: User, site_id: str, skip: int, limit: int) -> AttendancePageResponse:
        rows, total = AttendanceWorkspaceRepository.get_site_history(
            session=session, 
            company_id=current_user.company_id, 
            site_id=site_id, 
            skip=skip, 
            limit=limit
        )
        return cls._map_to_page_response(rows, total, skip, limit)
        
    @classmethod
    def get_contractor_history(cls, session: Session, current_user: User, contractor_id: str, skip: int, limit: int) -> AttendancePageResponse:
        rows, total = AttendanceWorkspaceRepository.get_contractor_history(
            session=session, 
            company_id=current_user.company_id, 
            contractor_id=contractor_id, 
            skip=skip, 
            limit=limit
        )
        return cls._map_to_page_response(rows, total, skip, limit)

    @classmethod
    def get_department_history(cls, session: Session, current_user: User, department_id: str, skip: int, limit: int) -> AttendancePageResponse:
        rows, total = AttendanceWorkspaceRepository.get_department_history(
            session=session, 
            company_id=current_user.company_id, 
            department_id=department_id, 
            skip=skip, 
            limit=limit
        )
        return cls._map_to_page_response(rows, total, skip, limit)
