from sqlalchemy.orm import Session
from app.models.models import User, UserRole, WorkerStatus, Site
from app.core.exceptions import ResourceNotFoundException, ValidationException, StateTransitionException
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class UserService:
    SEARCH_FIELDS = [User.name, User.employee_id, User.phone_number]
    
    SORTABLE_FIELDS = {
        "name": User.name,
        "status": User.status,
        "role": User.role,
        "phone_number": User.phone_number,
        "employee_id": User.employee_id,
    }

    @classmethod
    def get_users(cls, db: Session, tenant, query) -> tuple[List[User], int]:
        from app.services.query_helper import apply_search, apply_sort
        
        db_query = db.query(User).filter(User.role == UserRole.WORKER)
        db_query = db_query.filter(User.company_id == tenant.id)
        
        # Filtering
        if query.status:
            db_query = db_query.filter(User.status == query.status)
        if query.role:
            db_query = db_query.filter(User.role == query.role)
        if query.department_id:
            db_query = db_query.filter(User.department_id == query.department_id)
        if query.contractor_id:
            db_query = db_query.filter(User.contractor_id == query.contractor_id)
        # Assuming worker_to_site relationship handles site assignment
        if query.site_id:
            db_query = db_query.filter(User.assigned_sites.any(Site.id == query.site_id))
            
        # Searching
        db_query = apply_search(db_query, query.search, cls.SEARCH_FIELDS)
        
        # Count BEFORE Sort
        total_count = db_query.count()
        
        # Sorting
        db_query = apply_sort(
            db_query, 
            query.sort_by, 
            query.sort_order, 
            cls.SORTABLE_FIELDS, 
            default_sort_field="name",
            default_sort_order="asc"
        )
        
        items = db_query.offset(query.skip).limit(query.limit).all()
        return items, total_count

    @classmethod
    def get_user(cls, db: Session, user_id: str, current_user: User) -> User:
        query = db.query(User).filter(User.id == user_id)
        if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
            query = query.filter(User.company_id == current_user.company_id)
        user = query.first()
        if not user:
            raise ResourceNotFoundException("User not found")
        return user

    @classmethod
    def get_user_sites(cls, db: Session, user_id: str, current_user: User) -> List[Site]:
        user = cls.get_user(db, user_id, current_user)
        return user.assigned_sites

    @classmethod
    def update_worker_status(cls, db: Session, user_id: str, status: WorkerStatus, is_active: bool, admin: User) -> User:
        if user_id == admin.id and status == WorkerStatus.SUSPENDED:
            raise ValidationException("Cannot suspend yourself")
            
        query = db.query(User).filter(User.id == user_id)
        if admin.company_id:
            query = query.filter(User.company_id == admin.company_id)
        user = query.first()
        
        if not user:
            raise ResourceNotFoundException("User not found or access denied")
            
        if status == WorkerStatus.SUSPENDED and user.role in [UserRole.COMPANY_ADMIN, UserRole.SYSTEM_ADMIN]:
            raise ValidationException("Admin users cannot be suspended")

        if status == WorkerStatus.APPROVED and user.status == WorkerStatus.PENDING:
            missing_fields = []
            if not user.emergency_contact_name:
                missing_fields.append("emergency contact name")
            if not user.emergency_contact_phone:
                missing_fields.append("emergency contact phone")
            if not user.designation:
                missing_fields.append("designation")
                
            if missing_fields:
                missing_str = ", ".join(missing_fields)
                raise StateTransitionException(f"Worker missing required fields for approval: {missing_str}.")

        # If suspending, auto-checkout any active attendance sessions
        if status == WorkerStatus.SUSPENDED:
            from app.models.models import Attendance, AttendanceStatus
            from datetime import datetime, timezone
            active_sessions = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.status == AttendanceStatus.CHECKED_IN
            ).all()
            for session in active_sessions:
                session.status = AttendanceStatus.CHECKED_OUT
                session.check_out_time = datetime.now(timezone.utc)

        user.status = status
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        logger.info(f"Admin {admin.id} changed user {user_id} status to {status.value}")
        return user
