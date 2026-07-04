from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from app.models.models import User, Attendance, AttendanceCorrectionLog, GovernanceAction, AttendanceStatus, AttendanceReasonCode
from app.schemas.schemas import GovernanceResult
from app.services.attendance_service import AttendanceService

class AttendanceGovernanceService:
    @classmethod
    def _create_audit_log(
        cls,
        session: Session,
        attendance_id: str,
        correction_batch_id: str,
        attendance_version: int,
        governance_action: GovernanceAction,
        field_name: str,
        old_value: Optional[str],
        new_value: Optional[str],
        reason_code: AttendanceReasonCode,
        reason_notes: Optional[str],
        performed_by: User
    ) -> AttendanceCorrectionLog:
        log_entry = AttendanceCorrectionLog(
            attendance_id=attendance_id,
            correction_batch_id=correction_batch_id,
            attendance_version=attendance_version,
            governance_action=governance_action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            reason_code=reason_code,
            reason_notes=reason_notes,
            performed_by=performed_by.id,
            approved_by=performed_by.id # Simple implementation: performer is approver
        )
        session.add(log_entry)
        return log_entry

    @classmethod
    def administrative_checkout(
        cls,
        session: Session,
        attendance_id: str,
        performed_by: User,
        reason_code: str,
        reason_notes: Optional[str] = None
    ) -> Attendance:
        """
        Executes a manual checkout on behalf of a worker.
        """
        attendance = session.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError("Attendance record not found.")
            
        if attendance.status != AttendanceStatus.CHECKED_IN:
            raise ValueError("Can only perform administrative checkout on active attendances.")
            
        # Record old value
        old_status = attendance.status.value
        
        # Create a single batch for this governance operation
        batch_id = str(uuid.uuid4())
        
        # Mutate via AttendanceService (governance delegates state change)
        updated_attendance = AttendanceService.admin_force_checkout(
            session=session,
            attendance=attendance
        )
        
        # Create Generic Field-Level Audit
        cls._create_audit_log(
            session=session,
            attendance_id=updated_attendance.id,
            correction_batch_id=batch_id,
            attendance_version=updated_attendance.attendance_version,
            governance_action=GovernanceAction.ADMIN_CHECKOUT,
            field_name="status",
            old_value=old_status,
            new_value=updated_attendance.status.value,
            reason_code=reason_code,
            reason_notes=reason_notes,
            performed_by=performed_by
        )
        
        session.commit()
        
        return GovernanceResult(
            correction_batch_id=batch_id,
            attendance_version=updated_attendance.attendance_version,
            fields_modified=["status", "check_out_time", "check_out_method"],
            performed_at=datetime.now(timezone.utc)
        )

    @classmethod
    def correct_attendance(
        cls,
        session: Session,
        attendance_id: str,
        performed_by: User,
        reason_code: str,
        reason_notes: Optional[str] = None,
        new_check_in_time: Optional[datetime] = None,
        new_check_out_time: Optional[datetime] = None
    ) -> Attendance:
        """
        Corrects timestamps on an attendance record.
        Completed attendances must never transition back to CHECKED_IN.
        """
        attendance = session.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError("Attendance record not found.")

        if not new_check_in_time and not new_check_out_time:
            raise ValueError("Must provide at least one time to correct.")

        old_check_in = attendance.check_in_time.isoformat() if attendance.check_in_time else None
        old_check_out = attendance.check_out_time.isoformat() if attendance.check_out_time else None

        # Create a single batch for this governance operation
        batch_id = str(uuid.uuid4())
        fields_modified = []

        # Delegate mutation to AttendanceService
        updated_attendance = AttendanceService.update_times(
            session=session,
            attendance=attendance,
            check_in_time=new_check_in_time,
            check_out_time=new_check_out_time
        )

        if new_check_in_time:
            cls._create_audit_log(
                session=session,
                attendance_id=updated_attendance.id,
                correction_batch_id=batch_id,
                attendance_version=updated_attendance.attendance_version,
                governance_action=GovernanceAction.TIME_CORRECTION,
                field_name="check_in_time",
                old_value=old_check_in,
                new_value=new_check_in_time.isoformat(),
                reason_code=reason_code,
                reason_notes=reason_notes,
                performed_by=performed_by
            )
            fields_modified.append("check_in_time")
            
        if new_check_out_time:
            cls._create_audit_log(
                session=session,
                attendance_id=updated_attendance.id,
                correction_batch_id=batch_id,
                attendance_version=updated_attendance.attendance_version,
                governance_action=GovernanceAction.TIME_CORRECTION,
                field_name="check_out_time",
                old_value=old_check_out,
                new_value=new_check_out_time.isoformat(),
                reason_code=reason_code,
                reason_notes=reason_notes,
                performed_by=performed_by
            )
            fields_modified.append("check_out_time")
            
        session.commit()
        
        return GovernanceResult(
            correction_batch_id=batch_id,
            attendance_version=updated_attendance.attendance_version,
            fields_modified=fields_modified,
            performed_at=datetime.now(timezone.utc)
        )

    @classmethod
    def correction_history(
        cls,
        session: Session,
        attendance_id: str,
        performed_by: User
    ) -> List[AttendanceCorrectionLog]:
        """
        Returns the immutable audit history of an attendance record.
        """
        attendance = session.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError("Attendance record not found.")
            
        logs = session.query(AttendanceCorrectionLog)\
            .filter(AttendanceCorrectionLog.attendance_id == attendance_id)\
            .order_by(AttendanceCorrectionLog.performed_at.asc())\
            .all()
            
        return logs
