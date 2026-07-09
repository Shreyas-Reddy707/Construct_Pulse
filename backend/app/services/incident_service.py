from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence
import uuid

from app.models.models import (
    Incident, IncidentParticipant, IncidentEvidence, IncidentAuditLog,
    IncidentStatus, IncidentSeverity, ParticipantRole, EvidenceType, User, Site
)
from app.schemas.schemas import (
    IncidentCreate, IncidentResponse, IncidentParticipantCreate, IncidentParticipantResponse,
    IncidentEvidenceCreate, IncidentEvidenceResponse, IncidentStatusUpdate, IncidentAssign,
    IncidentDashboard, IncidentSummary
)

class IncidentService:
    @classmethod
    def _generate_incident_number(cls, db: Session, company_id: str) -> str:
        # A simple generation mechanism, e.g., INC-YYYY-UUID_prefix or similar
        year = datetime.now(timezone.utc).year
        # Concurrency-safe Incident Number Generation
        # We explicitly use a DB sequence to avoid race conditions inherent in MAX() or COUNT().
        seq_val = db.execute(Sequence('incident_number_seq')).scalar()
        return f"INC-{year}-{seq_val:06d}"

    @classmethod
    def _map_incident_to_dto(cls, incident: Incident) -> IncidentResponse:
        return IncidentResponse(
            id=incident.id,
            incident_number=incident.incident_number,
            company_id=incident.company_id,
            site_id=incident.site_id,
            reported_by=incident.reported_by,
            assigned_to=incident.assigned_to,
            severity=incident.severity,
            status=incident.status,
            title=incident.title,
            description=incident.description,
            reported_at=incident.reported_at,
            resolved_at=incident.resolved_at,
            closed_at=incident.closed_at,
            incident_version=incident.incident_version,
            incident_source=incident.incident_source
        )

    @classmethod
    def _map_participant_to_dto(cls, p: IncidentParticipant) -> IncidentParticipantResponse:
        return IncidentParticipantResponse(
            id=p.id,
            incident_id=p.incident_id,
            user_id=p.user_id,
            participant_name=p.participant_name,
            role=p.role,
            notes=p.notes,
            added_at=p.added_at
        )

    @classmethod
    def _map_evidence_to_dto(cls, e: IncidentEvidence) -> IncidentEvidenceResponse:
        return IncidentEvidenceResponse(
            id=e.id,
            incident_id=e.incident_id,
            evidence_type=e.evidence_type,
            reference=e.reference,
            description=e.description,
            uploaded_by=e.uploaded_by,
            uploaded_at=e.uploaded_at,
            evidence_version=e.evidence_version
        )

    @classmethod
    def _create_audit_log(cls, db: Session, incident_id: str, old_status: Optional[IncidentStatus], new_status: Optional[IncidentStatus], performed_by: str, reason: str):
        audit = IncidentAuditLog(
            incident_id=incident_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def create_incident(cls, db: Session, company_id: str, current_user_id: str, payload: IncidentCreate) -> IncidentResponse:
        from app.core.exceptions import ResourceNotFoundException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        site = db.query(Site).filter(Site.id == payload.site_id, Site.company_id == company_id).first()
        if not site:
            raise ResourceNotFoundException("Site not found or not in company")

        incident_number = cls._generate_incident_number(db, company_id)

        incident = Incident(
            incident_number=incident_number,
            company_id=company_id,
            site_id=payload.site_id,
            reported_by=current_user_id,
            severity=payload.severity,
            status=IncidentStatus.REPORTED,
            title=payload.title,
            description=payload.description
        )
        db.add(incident)
        db.flush()

        cls._create_audit_log(
            db, 
            incident.id, 
            None, 
            IncidentStatus.REPORTED, 
            current_user_id, 
            "Incident Reported"
        )
        
        db.commit()
        db.refresh(incident)
        return cls._map_incident_to_dto(incident)

    @classmethod
    def get_incident(cls, db: Session, company_id: str, incident_id: str) -> Optional[IncidentResponse]:
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if incident:
            return cls._map_incident_to_dto(incident)
        return None

    @classmethod
    def list_incidents(cls, db: Session, company_id: str, site_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[IncidentResponse]:
        query = db.query(Incident).filter(Incident.company_id == company_id)
        if site_id:
            query = query.filter(Incident.site_id == site_id)
        
        incidents = query.order_by(Incident.reported_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_incident_to_dto(inc) for inc in incidents]

    @classmethod
    def assign_investigator(cls, db: Session, company_id: str, incident_id: str, current_user_id: str, payload: IncidentAssign) -> IncidentResponse:
        from app.core.exceptions import ResourceNotFoundException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")

        investigator = db.query(User).filter(User.id == payload.assigned_to, User.company_id == company_id).first()
        if not investigator:
            raise ResourceNotFoundException("Assigned user not found in company")

        incident.assigned_to = payload.assigned_to
        incident.incident_version += 1 # Optimistic concurrency preparation

        if incident.status == IncidentStatus.REPORTED:
            cls._update_status_internal(db, incident, IncidentStatus.UNDER_INVESTIGATION, current_user_id, payload.reason)
        else:
            # Assignment History Clarification: All reassignment history is exclusively in IncidentAuditLog
            cls._create_audit_log(db, incident.id, incident.status, incident.status, current_user_id, f"Investigator assigned: {payload.reason}")
        
        db.commit()
        db.refresh(incident)
        return cls._map_incident_to_dto(incident)

    @classmethod
    def _update_status_internal(cls, db: Session, incident: Incident, new_status: IncidentStatus, current_user_id: str, reason: str):
        if incident.status == new_status:
            return

        old_status = incident.status
        incident.status = new_status

        if new_status == IncidentStatus.RESOLVED:
            incident.resolved_at = datetime.now(timezone.utc)
        elif new_status == IncidentStatus.CLOSED:
            incident.closed_at = datetime.now(timezone.utc)

        incident.incident_version += 1 # Optimistic concurrency preparation

        cls._create_audit_log(db, incident.id, old_status, new_status, current_user_id, reason)

    @classmethod
    def update_status(cls, db: Session, company_id: str, incident_id: str, current_user_id: str, payload: IncidentStatusUpdate) -> IncidentResponse:
        from app.core.exceptions import ResourceNotFoundException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")

        cls._update_status_internal(db, incident, payload.status, current_user_id, payload.reason)
        
        db.commit()
        db.refresh(incident)
        return cls._map_incident_to_dto(incident)

    @classmethod
    def add_participant(cls, db: Session, company_id: str, incident_id: str, current_user_id: str, payload: IncidentParticipantCreate) -> IncidentParticipantResponse:
        from app.core.exceptions import ResourceNotFoundException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")

        if payload.user_id:
            user = db.query(User).filter(User.id == payload.user_id, User.company_id == company_id).first()
            if not user:
                raise ResourceNotFoundException("Participant user not found in company")

        participant = IncidentParticipant(
            incident_id=incident.id,
            user_id=payload.user_id,
            participant_name=payload.participant_name,
            role=payload.role,
            notes=payload.notes
        )
        db.add(participant)
        
        incident.incident_version += 1 # Optimistic concurrency preparation
        cls._create_audit_log(db, incident.id, incident.status, incident.status, current_user_id, f"Added participant role {payload.role.value}")
        
        db.commit()
        db.refresh(participant)
        return cls._map_participant_to_dto(participant)

    @classmethod
    def add_evidence(cls, db: Session, company_id: str, incident_id: str, current_user_id: str, payload: IncidentEvidenceCreate) -> IncidentEvidenceResponse:
        from app.core.exceptions import ResourceNotFoundException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")

        evidence = IncidentEvidence(
            incident_id=incident.id,
            evidence_type=payload.evidence_type,
            reference=payload.reference,
            description=payload.description,
            uploaded_by=current_user_id
        )
        db.add(evidence)

        incident.incident_version += 1 # Optimistic concurrency preparation
        # Evidence Version Metadata: append-only evidence versioning exists purely to support future lifecycle evolution
        cls._create_audit_log(db, incident.id, incident.status, incident.status, current_user_id, f"Added evidence type {payload.evidence_type.value}")
        
        db.commit()
        db.refresh(evidence)
        return cls._map_evidence_to_dto(evidence)

    @classmethod
    def get_participants(cls, db: Session, company_id: str, incident_id: str) -> List[IncidentParticipantResponse]:
        from app.core.exceptions import ResourceNotFoundException
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")
        
        participants = db.query(IncidentParticipant).filter(IncidentParticipant.incident_id == incident_id).all()
        return [cls._map_participant_to_dto(p) for p in participants]

    @classmethod
    def get_evidence(cls, db: Session, company_id: str, incident_id: str) -> List[IncidentEvidenceResponse]:
        from app.core.exceptions import ResourceNotFoundException
        incident = db.query(Incident).filter(Incident.id == incident_id, Incident.company_id == company_id).first()
        if not incident:
            raise ResourceNotFoundException("Incident not found")
        
        evidence_list = db.query(IncidentEvidence).filter(IncidentEvidence.incident_id == incident_id).all()
        return [cls._map_evidence_to_dto(e) for e in evidence_list]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> IncidentDashboard:
        counts = db.query(
            Incident.status, 
            func.count(Incident.id)
        ).filter(
            Incident.company_id == company_id
        ).group_by(Incident.status).all()

        counts_dict = {status: count for status, count in counts}

        summary = IncidentSummary(
            draft=counts_dict.get(IncidentStatus.DRAFT, 0),
            reported=counts_dict.get(IncidentStatus.REPORTED, 0),
            under_investigation=counts_dict.get(IncidentStatus.UNDER_INVESTIGATION, 0),
            resolved=counts_dict.get(IncidentStatus.RESOLVED, 0),
            closed=counts_dict.get(IncidentStatus.CLOSED, 0)
        )

        return IncidentDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
