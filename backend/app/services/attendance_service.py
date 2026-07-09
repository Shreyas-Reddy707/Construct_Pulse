from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import User, Site, Attendance, AttendanceStatus, AttendanceMethod
from app.schemas.schemas import AccessDecision
from app.services.access_verification_service import AccessVerificationService
from app.services.secure_token_service import SecureTokenService

class AttendanceMethodResolver:
    """
    Translates an approved AccessDecision into the correct AttendanceMethod.
    This prepares the architecture for future access technologies.
    """
    @staticmethod
    def resolve(decision: AccessDecision, qr_token: Optional[str] = None) -> AttendanceMethod:
        if qr_token:
            return AttendanceMethod.SECURE_TOKEN
        # In future batches (e.g. RFID, BIOMETRICS), we can inspect the decision or context
        return AttendanceMethod.SYSTEM

class AttendanceService:
    MAX_DECISION_AGE_SECONDS = 30  # Configurable maximum age for decision freshness

    @classmethod
    def _get_worker_lock(cls, session: Session, user_id: str, lock: bool = False) -> User:
        query = session.query(User).filter(User.id == user_id)
        if lock:
            query = query.with_for_update()
        user = query.first()
        if not user:
            from app.core.exceptions import ResourceNotFoundException
            raise ResourceNotFoundException("Worker not found.")
        return user

    @classmethod
    def check_in(
        cls,
        session: Session,
        user: User,
        qr_token: Optional[str] = None,
        gps_latitude: Optional[float] = None,
        gps_longitude: Optional[float] = None
    ) -> Attendance:
        # 0. Acquire lock to serialize check-in attempts and prevent duplicate shifts
        cls._get_worker_lock(session, user.id, lock=True)
        
        active_attendance = session.query(Attendance).filter(
            Attendance.user_id == user.id,
            Attendance.status == AttendanceStatus.CHECKED_IN
        ).first()
        
        if active_attendance:
            from app.core.exceptions import ConflictException
            raise ConflictException(f"Worker is already checked in to a site (Site ID: {active_attendance.site_id}).")

        # 1. Access Verification (Orchestration)
        decision = AccessVerificationService.evaluate(
            session=session,
            user=user,
            qr_token=qr_token,
            gps_latitude=gps_latitude,
            gps_longitude=gps_longitude
        )
        
        if not decision.allowed:
            from app.core.exceptions import ValidationException, ResourceNotFoundException, StateTransitionException
            raise ValidationException(decision.reasons[0].message if decision.reasons else "Access denied.")
            
        # 2. Access Decision Freshness Validation
        if (datetime.now(timezone.utc) - decision.evaluated_at).total_seconds() > cls.MAX_DECISION_AGE_SECONDS:
            raise ValidationException("ACCESS_DECISION_EXPIRED: The access decision is no longer fresh.")
            
        # The site was successfully resolved during Access Verification.
        site = SecureTokenService.resolve_site(session, qr_token)
        if not site:
            raise ResourceNotFoundException("Site could not be resolved.")

        # 3. Resolve Attendance Method
        method = AttendanceMethodResolver.resolve(decision, qr_token)

        # 4. Resolve token metadata (for audit snapshot)
        token_id = None
        token_generation = None
        if qr_token:
            # We fetch minimal info for the snapshot; assuming token might be stored or tracked.
            # For this foundation, we can extract from SecureTokenService if available.
            pass

        # 5. Create Attendance
        attendance = Attendance(
            user_id=user.id,
            site_id=site.id,
            company_id=user.company_id,
            gps_latitude=gps_latitude,
            gps_longitude=gps_longitude,
            status=AttendanceStatus.CHECKED_IN,
            check_in_method=method,
            access_token_id=qr_token, # Snapshot token value/id
            access_generation=1,      # Snapshot placeholder for generation if tracked
            access_verified_at=decision.evaluated_at
        )
        
        session.add(attendance)
        session.commit()
        session.refresh(attendance)
        
        cls._emit_attendance_created(attendance)
        
        return attendance

    @classmethod
    def check_out(
        cls,
        session: Session,
        user: User,
        site_id: str
    ) -> Attendance:
        # 1. Locate active attendance with lock to serialize concurrent checkouts
        attendance = session.query(Attendance).filter(
            Attendance.user_id == user.id,
            Attendance.site_id == site_id,
            Attendance.status == AttendanceStatus.CHECKED_IN
        ).with_for_update().first()
        
        if not attendance:
            raise ResourceNotFoundException("Active check-in not found for this site.")
            
        # 2. Complete attendance
        attendance.check_out_time = datetime.now(timezone.utc)
        attendance.status = AttendanceStatus.CHECKED_OUT
        attendance.check_out_method = AttendanceMethod.SYSTEM  # Can be extended in future batches
        
        session.commit()
        session.refresh(attendance)
        
        cls._emit_attendance_completed(attendance)
        
        return attendance

    @classmethod
    def admin_force_checkout(
        cls,
        session: Session,
        attendance: Attendance,
        check_out_time: datetime = None
    ) -> Attendance:
        """
        Invoked ONLY by Governance Service.
        Mutates the attendance status to CHECKED_OUT and sets check_out_method.
        """
        if attendance.status != AttendanceStatus.CHECKED_IN:
            raise StateTransitionException("Attendance is already completed.")
            
        attendance.check_out_time = check_out_time or datetime.now(timezone.utc)
        attendance.status = AttendanceStatus.CHECKED_OUT
        attendance.check_out_method = AttendanceMethod.ADMIN_OVERRIDE
        attendance.attendance_version += 1
        
        session.flush()
        
        cls._emit_attendance_completed(attendance)
        
        return attendance

    @classmethod
    def update_times(
        cls,
        session: Session,
        attendance: Attendance,
        check_in_time: Optional[datetime] = None,
        check_out_time: Optional[datetime] = None
    ) -> Attendance:
        """
        Invoked ONLY by Governance Service.
        Mutates check_in_time and/or check_out_time.
        """
        if check_in_time:
            attendance.check_in_time = check_in_time
            
        if check_out_time:
            attendance.check_out_time = check_out_time
            if attendance.status == AttendanceStatus.CHECKED_IN:
                attendance.status = AttendanceStatus.CHECKED_OUT
                attendance.check_out_method = AttendanceMethod.ADMIN_OVERRIDE

        if check_in_time or check_out_time:
            attendance.attendance_version += 1
            
        session.flush()
        return attendance

    # --- Architecture Preparation for Future Domain Events ---
    @classmethod
    def _emit_attendance_created(cls, attendance: Attendance):
        """
        EXTENSION POINT: Emit Domain Event `AttendanceCreated`.
        (Do NOT implement event bus infrastructure in this batch.
         This hook strictly prepares the architecture.)
        """
        pass

    @classmethod
    def _emit_attendance_completed(cls, attendance: Attendance):
        """
        EXTENSION POINT: Emit Domain Event `AttendanceCompleted`.
        (Do NOT implement event bus infrastructure in this batch.
         This hook strictly prepares the architecture.)
        """
        pass

    @classmethod
    def get_my_today_attendance(cls, session: Session, user: User) -> dict:
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        all_today = session.query(Attendance).filter(
            Attendance.user_id == user.id,
            or_(
                Attendance.check_in_time >= today_start,
                Attendance.check_out_time.is_(None)
            )
        ).order_by(Attendance.check_in_time.asc()).all()
        
        hours_today = 0.0
        for a in all_today:
            out_time = a.check_out_time or datetime.now(timezone.utc)
            duration = (out_time - a.check_in_time).total_seconds() / 3600.0
            hours_today += duration
            
        latest_att = all_today[-1] if all_today else None
        
        if not latest_att:
            return {
                "checked_in": False,
                "site_id": None,
                "site_name": None,
                "check_in_time": None,
                "check_out_time": None,
                "hours_today": round(hours_today, 2)
            }
            
        return {
            "checked_in": latest_att.check_out_time is None,
            "site_id": latest_att.site_id,
            "site_name": latest_att.site_name,
            "check_in_time": latest_att.check_in_time.isoformat() if latest_att.check_in_time else None,
            "check_out_time": latest_att.check_out_time.isoformat() if latest_att.check_out_time else None,
            "hours_today": round(hours_today, 2)
        }

    @classmethod
    def get_worker_history(cls, session: Session, worker_id: str, company_id: Optional[str] = None) -> List[Attendance]:
        query = session.query(Attendance).filter(Attendance.user_id == worker_id)
        if company_id:
            query = query.filter(Attendance.company_id == company_id)
        return query.order_by(Attendance.check_in_time.desc()).all()

    @classmethod
    def get_live_attendance(cls, session: Session, company_id: Optional[str] = None) -> List[Attendance]:
        query = session.query(Attendance).filter(Attendance.check_out_time.is_(None))
        if company_id:
            query = query.filter(Attendance.company_id == company_id)
        return query.all()

    @classmethod
    def get_company_history(cls, session: Session, company_id: Optional[str] = None) -> List[Attendance]:
        query = session.query(Attendance)
        if company_id:
            query = query.filter(Attendance.company_id == company_id)
        return query.order_by(Attendance.check_in_time.desc()).all()
