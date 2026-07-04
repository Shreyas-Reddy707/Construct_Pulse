from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    SafetyObservation, CorrectiveAction, SafetyObservationAuditLog, 
    ObservationStatus, CorrectiveActionStatus, ObservationSource, CorrectiveActionSource,
    User, Site
)
from app.schemas.schemas import (
    SafetyObservationCreate, CorrectiveActionCreate,
    SafetyObservationResponse, CorrectiveActionResponse,
    SafetyDashboard, SafetySummary
)

class SafetyOperationsService:
    """
    Public Service Contract:
    SafetyOperationsService is the exclusive public interface for Safety Operations.
    Future domains MUST consume SafetyOperationsService.
    They must NEVER query SafetyObservation or CorrectiveAction directly.

    Architectural Documentation:
    - Observation: Root aggregate representing the safety report.
    - CorrectiveAction: Child work item belonging to an observation.
    - Verification: Confirms all corrective actions have been successfully completed.
    - Closing: Terminates the observation lifecycle.
    """
    @classmethod
    def _generate_observation_number(cls, db: Session) -> str:
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('safety_observation_number_seq')).scalar()
        return f"OBS-{year}-{seq_val:06d}"

    @classmethod
    def _map_action_to_dto(cls, action: CorrectiveAction) -> CorrectiveActionResponse:
        # Corrective Action Ownership Documentation: assigned_to represents only the CURRENT owner.
        return CorrectiveActionResponse(
            id=action.id,
            observation_id=action.observation_id,
            assigned_to=action.assigned_to,
            action_status=action.action_status,
            action_source=action.action_source,
            corrective_action_version=action.corrective_action_version,
            title=action.title,
            description=action.description,
            due_date=action.due_date,
            completed_at=action.completed_at,
            created_at=action.created_at
        )

    @classmethod
    def _map_observation_to_dto(cls, observation: SafetyObservation) -> SafetyObservationResponse:
        return SafetyObservationResponse(
            id=observation.id,
            observation_number=observation.observation_number,
            company_id=observation.company_id,
            site_id=observation.site_id,
            reported_by=observation.reported_by,
            assigned_to=observation.assigned_to,
            observation_type=observation.observation_type,
            severity=observation.severity,
            observation_status=observation.observation_status,
            observation_source=observation.observation_source,
            observation_version=observation.observation_version,
            title=observation.title,
            description=observation.description,
            created_at=observation.created_at,
            closed_at=observation.closed_at,
            verified_by=observation.verified_by,
            verified_at=observation.verified_at,
            actions=[cls._map_action_to_dto(a) for a in observation.actions]
        )

    @classmethod
    def _create_audit_log(cls, db: Session, observation_id: str, observation_version: int, observation_source: ObservationSource, audit_batch_id: str, old_status: Optional[ObservationStatus], new_status: Optional[ObservationStatus], performed_by: str, reason: str):
        audit = SafetyObservationAuditLog(
            observation_id=observation_id,
            observation_version=observation_version,
            observation_source=observation_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def create_observation(cls, db: Session, company_id: str, current_user_id: str, payload: SafetyObservationCreate) -> SafetyObservationResponse:
        site = db.query(Site).filter(Site.id == payload.site_id, Site.company_id == company_id).first()
        if not site:
            raise ValueError("Site not found")

        if payload.assigned_to:
            assignee = db.query(User).filter(User.id == payload.assigned_to, User.company_id == company_id).first()
            if not assignee:
                raise ValueError("Assignee not found")

        obs_number = cls._generate_observation_number(db)
        
        observation = SafetyObservation(
            observation_number=obs_number,
            company_id=company_id,
            site_id=payload.site_id,
            reported_by=current_user_id,
            assigned_to=payload.assigned_to,
            observation_type=payload.observation_type,
            severity=payload.severity,
            observation_status=ObservationStatus.REPORTED,
            observation_source=ObservationSource.MANUAL,
            title=payload.title,
            description=payload.description
        )
        db.add(observation)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=ObservationStatus.REPORTED,
            performed_by=current_user_id,
            reason="Safety observation reported"
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def assign_corrective_action(cls, db: Session, company_id: str, observation_id: str, current_user_id: str, payload: CorrectiveActionCreate) -> SafetyObservationResponse:
        observation = db.query(SafetyObservation).filter(SafetyObservation.id == observation_id, SafetyObservation.company_id == company_id).first()
        if not observation:
            raise ValueError("Observation not found")
        
        if observation.observation_status in [ObservationStatus.CLOSED, ObservationStatus.CANCELLED]:
            raise ValueError("Cannot assign action to closed or cancelled observation")

        assignee = db.query(User).filter(User.id == payload.assigned_to, User.company_id == company_id).first()
        if not assignee:
            raise ValueError("Assignee not found")

        action = CorrectiveAction(
            observation_id=observation.id,
            assigned_to=payload.assigned_to,
            action_status=CorrectiveActionStatus.OPEN,
            title=payload.title,
            description=payload.description,
            due_date=payload.due_date
        )
        db.add(action)

        old_status = observation.observation_status
        if observation.observation_status == ObservationStatus.REPORTED:
            observation.observation_status = ObservationStatus.IN_PROGRESS
        
        observation.observation_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=observation.observation_status,
            performed_by=current_user_id,
            reason=f"Assigned corrective action: {payload.title}"
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def update_observation_status(cls, db: Session, company_id: str, observation_id: str, current_user_id: str, status: ObservationStatus, reason: str) -> SafetyObservationResponse:
        observation = db.query(SafetyObservation).filter(SafetyObservation.id == observation_id, SafetyObservation.company_id == company_id).first()
        if not observation:
            raise ValueError("Observation not found")
        
        if observation.observation_status in [ObservationStatus.CLOSED, ObservationStatus.CANCELLED]:
            raise ValueError("Cannot update status of closed or cancelled observation")

        if status == ObservationStatus.CLOSED:
            raise ValueError("Use close_observation to close an observation")
        if status == ObservationStatus.VERIFIED:
            raise ValueError("Use verify_observation to verify an observation")

        old_status = observation.observation_status
        observation.observation_status = status
        observation.observation_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=observation.observation_status,
            performed_by=current_user_id,
            reason=reason
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def update_corrective_action_status(cls, db: Session, company_id: str, action_id: str, current_user_id: str, status: CorrectiveActionStatus, reason: str) -> SafetyObservationResponse:
        action = db.query(CorrectiveAction).join(SafetyObservation).filter(
            CorrectiveAction.id == action_id,
            SafetyObservation.company_id == company_id
        ).first()
        if not action:
            raise ValueError("Corrective action not found")

        observation = action.observation
        if observation.observation_status in [ObservationStatus.CLOSED, ObservationStatus.CANCELLED]:
            raise ValueError("Cannot update action for a closed or cancelled observation")

        action.action_status = status
        if status == CorrectiveActionStatus.COMPLETED:
            action.completed_at = datetime.now(timezone.utc)
        action.corrective_action_version += 1

        observation.observation_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=observation.observation_status,
            new_status=observation.observation_status,
            performed_by=current_user_id,
            reason=f"Corrective action status updated to {status.value}: {reason}"
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def verify_observation(cls, db: Session, company_id: str, observation_id: str, current_user_id: str, reason: str) -> SafetyObservationResponse:
        observation = db.query(SafetyObservation).filter(SafetyObservation.id == observation_id, SafetyObservation.company_id == company_id).first()
        if not observation:
            raise ValueError("Observation not found")
        
        if observation.observation_status in [ObservationStatus.CLOSED, ObservationStatus.CANCELLED]:
            raise ValueError("Cannot verify closed or cancelled observation")
        
        # Ensure all actions are completed or cancelled
        open_actions = [a for a in observation.actions if a.action_status in [CorrectiveActionStatus.OPEN, CorrectiveActionStatus.IN_PROGRESS]]
        if open_actions:
            raise ValueError("Cannot verify observation with open corrective actions")

        old_status = observation.observation_status
        observation.observation_status = ObservationStatus.VERIFIED
        observation.verified_by = current_user_id
        observation.verified_at = datetime.now(timezone.utc)
        observation.observation_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=observation.observation_status,
            performed_by=current_user_id,
            reason=f"Observation verified: {reason}"
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def close_observation(cls, db: Session, company_id: str, observation_id: str, current_user_id: str, reason: str) -> SafetyObservationResponse:
        observation = db.query(SafetyObservation).filter(SafetyObservation.id == observation_id, SafetyObservation.company_id == company_id).first()
        if not observation:
            raise ValueError("Observation not found")

        if observation.observation_status != ObservationStatus.VERIFIED:
            raise ValueError("Only VERIFIED observations can be closed")

        old_status = observation.observation_status
        observation.observation_status = ObservationStatus.CLOSED
        observation.closed_at = datetime.now(timezone.utc)
        observation.observation_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            observation_id=observation.id,
            observation_version=observation.observation_version,
            observation_source=observation.observation_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=observation.observation_status,
            performed_by=current_user_id,
            reason=f"Observation closed: {reason}"
        )
        db.commit()
        db.refresh(observation)
        return cls._map_observation_to_dto(observation)

    @classmethod
    def get_observation(cls, db: Session, company_id: str, observation_id: str) -> Optional[SafetyObservationResponse]:
        observation = db.query(SafetyObservation).filter(SafetyObservation.id == observation_id, SafetyObservation.company_id == company_id).first()
        if observation:
            return cls._map_observation_to_dto(observation)
        return None

    @classmethod
    def list_observations(cls, db: Session, company_id: str, site_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[SafetyObservationResponse]:
        query = db.query(SafetyObservation).filter(SafetyObservation.company_id == company_id)
        if site_id:
            query = query.filter(SafetyObservation.site_id == site_id)
        
        observations = query.order_by(SafetyObservation.created_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_observation_to_dto(o) for o in observations]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> SafetyDashboard:
        counts = db.query(
            SafetyObservation.observation_status, 
            func.count(SafetyObservation.id)
        ).filter(
            SafetyObservation.company_id == company_id
        ).group_by(SafetyObservation.observation_status).all()

        counts_dict = {status: count for status, count in counts}

        summary = SafetySummary(
            reported=counts_dict.get(ObservationStatus.REPORTED, 0),
            in_progress=counts_dict.get(ObservationStatus.IN_PROGRESS, 0),
            verified=counts_dict.get(ObservationStatus.VERIFIED, 0),
            closed=counts_dict.get(ObservationStatus.CLOSED, 0),
            cancelled=counts_dict.get(ObservationStatus.CANCELLED, 0)
        )

        return SafetyDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
