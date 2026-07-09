from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    VisitorVisit, VisitorVisitAuditLog, VisitorVisitStatus, VisitSource, User, Site, IdentityType
)
from app.schemas.schemas import (
    VisitorVisitCreate, VisitorVisitResponse, VisitorDashboard, VisitorVisitSummary
)
from app.services.attendance_service import AttendanceService

class VisitorService:
    """
    Public Service Contract:
    VisitorService is the exclusive public interface for Visitor Management.
    Future domains MUST consume VisitorService and NEVER query VisitorVisit directly.
    """
    @classmethod
    def _generate_visit_number(cls, db: Session) -> str:
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('visitor_visit_number_seq')).scalar()
        return f"VIS-{year}-{seq_val:06d}"

    @classmethod
    def _map_visit_to_dto(cls, visit: VisitorVisit) -> VisitorVisitResponse:
        return VisitorVisitResponse(
            id=visit.id,
            visit_number=visit.visit_number,
            visitor_id=visit.visitor_id,
            host_id=visit.host_id,
            company_id=visit.company_id,
            site_id=visit.site_id,
            visit_status=visit.visit_status,
            visit_source=visit.visit_source,
            visit_version=visit.visit_version,
            purpose=visit.purpose,
            valid_from=visit.valid_from,
            valid_until=visit.valid_until,
            checked_in_at=visit.checked_in_at,
            checked_out_at=visit.checked_out_at,
            badge_identifier=visit.badge_identifier,
            created_at=visit.created_at
        )

    @classmethod
    def _create_audit_log(cls, db: Session, visit_id: str, old_status: Optional[VisitorVisitStatus], new_status: Optional[VisitorVisitStatus], performed_by: str, reason: str, visit_version: int, audit_batch_id: str):
        # Visit Audit Version Snapshot: captures the exact lifecycle version of the visit at this exact moment.
        audit = VisitorVisitAuditLog(
            visit_id=visit_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason,
            visit_version=visit_version,
            audit_batch_id=audit_batch_id
        )
        db.add(audit)

    @classmethod
    def register_visit(cls, db: Session, company_id: str, current_user_id: str, payload: VisitorVisitCreate) -> VisitorVisitResponse:
        from app.core.exceptions import ResourceNotFoundException, ValidationException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        # Validate site
        site = db.query(Site).filter(Site.id == payload.site_id, Site.company_id == company_id).first()
        if not site:
            raise ResourceNotFoundException("Site not found")

        # Validate visitor identity exists and is a VISITOR type
        visitor = db.query(User).filter(User.id == payload.visitor_id, User.company_id == company_id, User.identity_type == IdentityType.VISITOR).first()
        if not visitor:
            raise ValidationException("Invalid visitor identity")

        # Validate host
        host = db.query(User).filter(User.id == payload.host_id, User.company_id == company_id).first()
        if not host:
            raise ValidationException("Invalid host identity")

        visit_number = cls._generate_visit_number(db)
        visit_source = payload.visit_source if payload.visit_source == VisitSource.SELF_SERVICE else VisitSource.HOST
        
        # Visit Validity Documentation:
        # valid_from and valid_until represent authorization periods.
        # checked_in_at and checked_out_at represent actual physical presence.
        visit = VisitorVisit(
            visit_number=visit_number,
            visitor_id=payload.visitor_id,
            host_id=payload.host_id,
            company_id=company_id,
            site_id=payload.site_id,
            visit_status=VisitorVisitStatus.REQUESTED,
            visit_source=visit_source,
            purpose=payload.purpose,
            valid_from=payload.valid_from,
            valid_until=payload.valid_until
        )
        db.add(visit)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=None,
            new_status=VisitorVisitStatus.REQUESTED,
            performed_by=current_user_id,
            reason="Visit registered",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def approve_visit(cls, db: Session, company_id: str, visit_id: str, current_user_id: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status != VisitorVisitStatus.REQUESTED:
            raise StateTransitionException("Only REQUESTED visits can be approved")

        old_status = visit.visit_status
        visit.visit_status = VisitorVisitStatus.APPROVED
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason="Visit approved by host or admin",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def deny_visit(cls, db: Session, company_id: str, visit_id: str, current_user_id: str, reason: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status != VisitorVisitStatus.REQUESTED:
            raise StateTransitionException("Only REQUESTED visits can be denied")

        old_status = visit.visit_status
        visit.visit_status = VisitorVisitStatus.DENIED
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason=f"Visit denied: {reason}",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def cancel_visit(cls, db: Session, company_id: str, visit_id: str, current_user_id: str, reason: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status not in [VisitorVisitStatus.REQUESTED, VisitorVisitStatus.APPROVED]:
            raise StateTransitionException("Only REQUESTED or APPROVED visits can be cancelled")

        old_status = visit.visit_status
        # Visit Lifecycle Documentation: CANCELLED means visit intentionally terminated by a user.
        visit.visit_status = VisitorVisitStatus.CANCELLED
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason=f"Visit cancelled: {reason}",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def check_in(cls, db: Session, company_id: str, visit_id: str, current_user_id: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status != VisitorVisitStatus.APPROVED:
            raise StateTransitionException("Visit must be APPROVED to check-in")
            
        now_utc = datetime.now(timezone.utc)
        if visit.valid_until and now_utc > visit.valid_until:
            raise StateTransitionException("Visit validity period has expired")

        # Invoke AttendanceService to enforce check-in and update attendance ownership records
        from app.schemas.schemas import AttendancePunch
        from app.models.models import AttendanceMethod
        punch_payload = AttendancePunch(
            worker_id=visit.visitor_id,
            site_id=visit.site_id,
            method=AttendanceMethod.MANUAL
        )
        AttendanceService.record_punch(db, company_id, punch_payload)

        old_status = visit.visit_status
        visit.visit_status = VisitorVisitStatus.ACTIVE
        visit.checked_in_at = now_utc
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason="Visitor checked in",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def check_out(cls, db: Session, company_id: str, visit_id: str, current_user_id: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status != VisitorVisitStatus.ACTIVE:
            raise StateTransitionException("Visit must be ACTIVE to check-out")
        
        # Invoke AttendanceService to enforce check-out and update attendance ownership records
        from app.schemas.schemas import AttendancePunch
        from app.models.models import AttendanceMethod
        punch_payload = AttendancePunch(
            worker_id=visit.visitor_id,
            site_id=visit.site_id,
            method=AttendanceMethod.MANUAL
        )
        AttendanceService.record_punch(db, company_id, punch_payload)

        old_status = visit.visit_status
        visit.visit_status = VisitorVisitStatus.COMPLETED
        visit.checked_out_at = datetime.now(timezone.utc)
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason="Visitor checked out",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def get_visit(cls, db: Session, company_id: str, visit_id: str) -> Optional[VisitorVisitResponse]:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        if visit:
            return cls._map_visit_to_dto(visit)
        return None

    @classmethod
    def list_visits(cls, db: Session, company_id: str, site_id: Optional[str] = None, host_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[VisitorVisitResponse]:
        query = db.query(VisitorVisit).filter(VisitorVisit.company_id == company_id)
        if site_id:
            query = query.filter(VisitorVisit.site_id == site_id)
        if host_id:
            query = query.filter(VisitorVisit.host_id == host_id)
        
        visits = query.order_by(VisitorVisit.created_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_visit_to_dto(v) for v in visits]

    @classmethod
    def expire_visit(cls, db: Session, company_id: str, visit_id: str, current_user_id: str) -> VisitorVisitResponse:
        visit = db.query(VisitorVisit).filter(VisitorVisit.id == visit_id, VisitorVisit.company_id == company_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not visit:
            raise ResourceNotFoundException("Visit not found")
            
        if visit.visit_status not in [VisitorVisitStatus.REQUESTED, VisitorVisitStatus.APPROVED]:
            raise StateTransitionException("Only un-arrived visits can be expired")
            
        now_utc = datetime.now(timezone.utc)
        if visit.valid_until and now_utc <= visit.valid_until:
            raise StateTransitionException("Visit validity period has not expired yet")

        old_status = visit.visit_status
        # Visit Lifecycle Documentation: EXPIRED means visitor never successfully arrived before validity expired.
        visit.visit_status = VisitorVisitStatus.EXPIRED
        visit.visit_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            visit_id=visit.id,
            old_status=old_status,
            new_status=visit.visit_status,
            performed_by=current_user_id,
            reason="Visit expired",
            visit_version=visit.visit_version,
            audit_batch_id=audit_batch_id
        )
        db.commit()
        db.refresh(visit)
        return cls._map_visit_to_dto(visit)

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> VisitorDashboard:
        counts = db.query(
            VisitorVisit.visit_status, 
            func.count(VisitorVisit.id)
        ).filter(
            VisitorVisit.company_id == company_id
        ).group_by(VisitorVisit.visit_status).all()

        counts_dict = {status: count for status, count in counts}

        summary = VisitorVisitSummary(
            requested=counts_dict.get(VisitorVisitStatus.REQUESTED, 0),
            approved=counts_dict.get(VisitorVisitStatus.APPROVED, 0),
            active=counts_dict.get(VisitorVisitStatus.ACTIVE, 0),
            completed=counts_dict.get(VisitorVisitStatus.COMPLETED, 0),
            cancelled=counts_dict.get(VisitorVisitStatus.CANCELLED, 0),
            expired=counts_dict.get(VisitorVisitStatus.EXPIRED, 0)
        )

        return VisitorDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
