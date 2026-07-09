from sqlalchemy.orm import Session
from app.models.models import User, UserRole, WorkerStatus, Site
from app.core.exceptions import ResourceNotFoundException, ValidationException, StateTransitionException
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    def get_users(cls, db: Session, tenant, status: Optional[WorkerStatus], skip: int = 0, limit: int = 100) -> List[User]:
        query = db.query(User).filter(User.role == UserRole.WORKER)
        query = query.filter(User.company_id == tenant.id)
        if status:
            query = query.filter(User.status == status)
        return query.offset(skip).limit(limit).all()

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
        db.refresh(user)
        logger.info(f"Admin {admin.id} changed user {user_id} status to {status.value}")
        return user
