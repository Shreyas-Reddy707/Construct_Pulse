from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    SafetyCommunication, CommunicationAcknowledgement, CommunicationAuditLog,
    CommunicationStatus, CommunicationSource, User, Site
)
from app.schemas.schemas import (
    CommunicationCreate, CommunicationResponse, CommunicationAcknowledgementResponse,
    CommunicationDashboard, CommunicationSummary
)

class SafetyCommunicationService:
    """
    Public Service Contract:
    SafetyCommunicationService is the exclusive public interface for the Safety Communication Foundation.
    Future modules must consume this service and never query the underlying ORM models directly.
    """

    @classmethod
    def _generate_communication_number(cls, db: Session) -> str:
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('communication_number_seq')).scalar()
        return f"COM-{year}-{seq_val:06d}"

    @classmethod
    def _map_acknowledgement_to_dto(cls, ack: CommunicationAcknowledgement) -> CommunicationAcknowledgementResponse:
        # Architectural Documentation: Acknowledgements snapshot a specific communication_version.
        # Historical acknowledgements remain legally valid even if future versions exist.
        return CommunicationAcknowledgementResponse(
            id=ack.id,
            communication_id=ack.communication_id,
            user_id=ack.user_id,
            acknowledged_at=ack.acknowledged_at,
            communication_version=ack.communication_version
        )

    @classmethod
    def _map_communication_to_dto(cls, communication: SafetyCommunication) -> CommunicationResponse:
        return CommunicationResponse(
            id=communication.id,
            company_id=communication.company_id,
            site_id=communication.site_id,
            author_id=communication.author_id,
            communication_number=communication.communication_number,
            communication_version=communication.communication_version,
            communication_source=communication.communication_source,
            status=communication.status,
            title=communication.title,
            content=communication.content,
            requires_acknowledgement=communication.requires_acknowledgement,
            created_at=communication.created_at,
            published_at=communication.published_at,
            archived_at=communication.archived_at,
            acknowledgements=[cls._map_acknowledgement_to_dto(ack) for ack in communication.acknowledgements]
        )

    @classmethod
    def _create_audit_log(cls, db: Session, communication_id: str, communication_version: int, communication_source: CommunicationSource, audit_batch_id: str, old_status: Optional[CommunicationStatus], new_status: Optional[CommunicationStatus], performed_by: str, reason: str):
        # Architectural Documentation: Audit logs are append-only to preserve a verifiable chain of custody for all state changes.
        audit = CommunicationAuditLog(
            communication_id=communication_id,
            communication_version=communication_version,
            communication_source=communication_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def create_draft(cls, db: Session, company_id: str, current_user_id: str, payload: CommunicationCreate) -> CommunicationResponse:
        from app.core.exceptions import ResourceNotFoundException, ValidationException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        if payload.site_id:
            site = db.query(Site).filter(Site.id == payload.site_id, Site.company_id == company_id).first()
            if not site:
                raise ResourceNotFoundException("Site not found")

        # Architectural Documentation: Sequence generation is database-driven to ensure gapless, atomic sequence numbers even under concurrent load.
        comm_number = cls._generate_communication_number(db)

        # Architectural Documentation: communication_source exists to differentiate manual creation from automated system imports or API integrations.
        communication = SafetyCommunication(
            company_id=company_id,
            site_id=payload.site_id,
            author_id=current_user_id,
            communication_number=comm_number,
            communication_source=CommunicationSource.MANUAL,
            status=CommunicationStatus.DRAFT,
            title=payload.title,
            content=payload.content,
            requires_acknowledgement=payload.requires_acknowledgement
        )
        db.add(communication)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            communication_id=communication.id,
            communication_version=communication.communication_version,
            communication_source=communication.communication_source,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=CommunicationStatus.DRAFT,
            performed_by=current_user_id,
            reason="Communication draft created"
        )
        db.commit()
        db.refresh(communication)
        return cls._map_communication_to_dto(communication)

    @classmethod
    def publish(cls, db: Session, company_id: str, communication_id: str, current_user_id: str, reason: str) -> CommunicationResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        communication = db.query(SafetyCommunication).filter(SafetyCommunication.id == communication_id, SafetyCommunication.company_id == company_id).first()
        if not communication:
            raise ResourceNotFoundException("Communication not found")

        if communication.status != CommunicationStatus.DRAFT:
            raise StateTransitionException("Only DRAFT communications can be published")

        # Lifecycle Documentation: PUBLISHED
        # Published communications are made visible to the workforce.
        # They are entirely immutable to maintain legal and safety compliance.
        old_status = communication.status
        communication.status = CommunicationStatus.PUBLISHED
        communication.published_at = datetime.now(timezone.utc)
        
        # Verify communication_version increments consistently for every state-changing operation
        communication.communication_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            communication_id=communication.id,
            communication_version=communication.communication_version,
            communication_source=communication.communication_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=communication.status,
            performed_by=current_user_id,
            reason=f"Communication published: {reason}"
        )
        db.commit()
        db.refresh(communication)
        return cls._map_communication_to_dto(communication)

    @classmethod
    def archive(cls, db: Session, company_id: str, communication_id: str, current_user_id: str, reason: str) -> CommunicationResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        communication = db.query(SafetyCommunication).filter(SafetyCommunication.id == communication_id, SafetyCommunication.company_id == company_id).first()
        if not communication:
            raise ResourceNotFoundException("Communication not found")

        if communication.status != CommunicationStatus.PUBLISHED:
            raise StateTransitionException("Only PUBLISHED communications can be archived")

        # Lifecycle Documentation: ARCHIVED
        # Archived exists to retire a communication from active dashboards while maintaining its historical record.
        old_status = communication.status
        communication.status = CommunicationStatus.ARCHIVED
        communication.archived_at = datetime.now(timezone.utc)
        
        # Verify communication_version increments consistently for every state-changing operation
        communication.communication_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            communication_id=communication.id,
            communication_version=communication.communication_version,
            communication_source=communication.communication_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=communication.status,
            performed_by=current_user_id,
            reason=f"Communication archived: {reason}"
        )
        db.commit()
        db.refresh(communication)
        return cls._map_communication_to_dto(communication)

    @classmethod
    def acknowledge(cls, db: Session, company_id: str, communication_id: str, current_user_id: str) -> CommunicationResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, ValidationException, ConflictException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        communication = db.query(SafetyCommunication).filter(SafetyCommunication.id == communication_id, SafetyCommunication.company_id == company_id).first()
        if not communication:
            raise ResourceNotFoundException("Communication not found")

        if communication.status != CommunicationStatus.PUBLISHED:
            raise StateTransitionException("Can only acknowledge PUBLISHED communications")
            
        if not communication.requires_acknowledgement:
            raise ValidationException("This communication does not require acknowledgement")

        existing_ack = db.query(CommunicationAcknowledgement).filter(
            CommunicationAcknowledgement.communication_id == communication.id,
            CommunicationAcknowledgement.user_id == current_user_id
        ).first()

        if existing_ack:
            raise ConflictException("User has already acknowledged this communication")

        ack = CommunicationAcknowledgement(
            communication_id=communication.id,
            user_id=current_user_id,
            communication_version=communication.communication_version
        )
        db.add(ack)
        db.commit()
        db.refresh(communication)
        return cls._map_communication_to_dto(communication)

    @classmethod
    def get_communication(cls, db: Session, company_id: str, communication_id: str) -> Optional[CommunicationResponse]:
        communication = db.query(SafetyCommunication).filter(SafetyCommunication.id == communication_id, SafetyCommunication.company_id == company_id).first()
        if communication:
            return cls._map_communication_to_dto(communication)
        return None

    @classmethod
    def list_communications(cls, db: Session, company_id: str, site_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[CommunicationResponse]:
        query = db.query(SafetyCommunication).filter(SafetyCommunication.company_id == company_id)
        if site_id:
            query = query.filter(SafetyCommunication.site_id == site_id)
        
        communications = query.order_by(SafetyCommunication.created_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_communication_to_dto(c) for c in communications]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> CommunicationDashboard:
        counts = db.query(
            SafetyCommunication.status, 
            func.count(SafetyCommunication.id)
        ).filter(
            SafetyCommunication.company_id == company_id
        ).group_by(SafetyCommunication.status).all()

        counts_dict = {status: count for status, count in counts}

        req_ack = db.query(func.count(SafetyCommunication.id)).filter(
            SafetyCommunication.company_id == company_id,
            SafetyCommunication.requires_acknowledgement == True,
            SafetyCommunication.status == CommunicationStatus.PUBLISHED
        ).scalar() or 0

        summary = CommunicationSummary(
            draft=counts_dict.get(CommunicationStatus.DRAFT, 0),
            published=counts_dict.get(CommunicationStatus.PUBLISHED, 0),
            archived=counts_dict.get(CommunicationStatus.ARCHIVED, 0),
            requiring_acknowledgement=req_ack
        )

        return CommunicationDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
