from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import (
    MusterSession, MusterParticipant, MusterAuditLog,
    MusterSessionStatus, MusterParticipantStatus, MusterParticipantType,
    IdentityType, SnapshotSource
)
from app.schemas.schemas import (
    MusterSessionCreate, MusterSessionResponse, MusterParticipantResponse,
    MusterDashboard, MusterSummary, MusterOverrideRequest
)
from app.services.occupancy_service import OccupancyService

class EmergencyMusterService:
    
    @staticmethod
    def _map_identity_to_participant_type(identity_type_str: str) -> MusterParticipantType:
        try:
            identity_type = IdentityType(identity_type_str)
        except ValueError:
            return MusterParticipantType.WORKER

        mapping = {
            IdentityType.WORKER: MusterParticipantType.WORKER,
            IdentityType.VISITOR: MusterParticipantType.VISITOR,
            IdentityType.CONTRACTOR_REPRESENTATIVE: MusterParticipantType.CONTRACTOR,
            IdentityType.SITE_ENGINEER: MusterParticipantType.ENGINEER,
            IdentityType.INSPECTOR: MusterParticipantType.INSPECTOR,
            IdentityType.VENDOR: MusterParticipantType.CONTRACTOR
        }
        return mapping.get(identity_type, MusterParticipantType.WORKER)

    @classmethod
    def _map_session_to_dto(cls, session: MusterSession) -> MusterSessionResponse:
        return MusterSessionResponse(
            id=session.id,
            site_id=session.site_id,
            company_id=session.company_id,
            emergency_type=session.emergency_type,
            notes=session.notes,
            occupancy_snapshot_id=session.occupancy_snapshot_id,
            initiated_by=session.initiated_by,
            started_at=session.started_at,
            completed_at=session.completed_at,
            cancelled_at=session.cancelled_at,
            status=session.status
        )

    @classmethod
    def _map_participant_to_dto(cls, p: MusterParticipant) -> MusterParticipantResponse:
        return MusterParticipantResponse(
            id=p.id,
            muster_session_id=p.muster_session_id,
            attendance_id=p.attendance_id,
            user_id=p.user_id,
            participant_type=p.participant_type,
            status=p.status,
            acknowledged_at=p.acknowledged_at,
            acknowledged_by=p.acknowledged_by
        )

    @classmethod
    def create_session(cls, db: Session, company_id: str, current_user_id: str, create_dto: MusterSessionCreate) -> MusterSessionResponse:
        """
        Creates a new emergency muster session, captures the occupancy snapshot, 
        generates participants via bulk insert, and activates the session.
        """
        # 1. Create Session in DRAFT
        new_session = MusterSession(
            company_id=company_id,
            site_id=create_dto.site_id,
            initiated_by=current_user_id,
            emergency_type=create_dto.emergency_type,
            notes=create_dto.notes,
            status=MusterSessionStatus.DRAFT
        )
        db.add(new_session)
        db.flush()

        # 2. Capture Occupancy Snapshot
        snapshot_dto = OccupancyService.capture_snapshot(
            db, 
            site_id=create_dto.site_id, 
            captured_by=current_user_id, 
            source=SnapshotSource.SYSTEM
        )
        new_session.occupancy_snapshot_id = snapshot_dto.snapshot_id

        # 3. Generate Participants (High Performance Bulk Insert via Public Contract)
        from app.schemas.schemas import OccupancyQuery
        from app.services.occupancy_service import OccupancyService as OS
        
        # We explicitly consume the public read contract of OccupancyService
        # rather than directly orchestrating ORM entities owned by another domain.
        query = OccupancyQuery(site_id=create_dto.site_id, include_visitors=True, limit=100000)
        occupants = OS.get_muster_list(db, query)

        participants_to_insert = []
        for occupant in occupants:
            participants_to_insert.append(
                MusterParticipant(
                    muster_session_id=new_session.id,
                    attendance_id=occupant.attendance_id,
                    user_id=occupant.worker_id,
                    participant_type=cls._map_identity_to_participant_type(occupant.identity_type),
                    status=MusterParticipantStatus.UNACCOUNTED
                )
            )

        if participants_to_insert:
            db.bulk_save_objects(participants_to_insert)

        # 4. Transition to ACTIVE
        new_session.status = MusterSessionStatus.ACTIVE
        db.commit()
        db.refresh(new_session)

        return cls._map_session_to_dto(new_session)

    @classmethod
    def get_session(cls, db: Session, session_id: str) -> Optional[MusterSessionResponse]:
        session = db.query(MusterSession).filter(MusterSession.id == session_id).first()
        if session:
            return cls._map_session_to_dto(session)
        return None

    @classmethod
    def list_active_sessions(cls, db: Session, company_id: str, site_id: Optional[str] = None) -> List[MusterSessionResponse]:
        query = db.query(MusterSession).filter(
            MusterSession.company_id == company_id,
            MusterSession.status == MusterSessionStatus.ACTIVE
        )
        if site_id:
            query = query.filter(MusterSession.site_id == site_id)
        
        sessions = query.order_by(MusterSession.started_at.desc()).all()
        return [cls._map_session_to_dto(s) for s in sessions]

    @classmethod
    def complete_session(cls, db: Session, session_id: str, current_user_id: str) -> MusterSessionResponse:
        session = db.query(MusterSession).filter(MusterSession.id == session_id).first()
        if not session or session.status != MusterSessionStatus.ACTIVE:
            raise ValueError("Session not found or not active")

        session.status = MusterSessionStatus.COMPLETED
        session.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(session)
        return cls._map_session_to_dto(session)

    @classmethod
    def cancel_session(cls, db: Session, session_id: str, current_user_id: str) -> MusterSessionResponse:
        session = db.query(MusterSession).filter(MusterSession.id == session_id).first()
        if not session or session.status != MusterSessionStatus.ACTIVE:
            raise ValueError("Session not found or not active")

        session.status = MusterSessionStatus.CANCELLED
        session.cancelled_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(session)
        return cls._map_session_to_dto(session)

    @classmethod
    def get_participants(cls, db: Session, session_id: str, skip: int = 0, limit: int = 100) -> List[MusterParticipantResponse]:
        participants = db.query(MusterParticipant).filter(
            MusterParticipant.muster_session_id == session_id
        ).offset(skip).limit(limit).all()
        return [cls._map_participant_to_dto(p) for p in participants]

    @classmethod
    def acknowledge_participant(cls, db: Session, participant_id: str, current_user_id: str) -> MusterParticipantResponse:
        return cls._update_participant_status(
            db, participant_id, current_user_id, 
            MusterParticipantStatus.SAFE, "Self or direct acknowledgement"
        )

    @classmethod
    def manager_override(cls, db: Session, participant_id: str, current_user_id: str, override: MusterOverrideRequest) -> MusterParticipantResponse:
        return cls._update_participant_status(
            db, participant_id, current_user_id, 
            override.status, override.reason or "Manager Override"
        )

    @classmethod
    def _update_participant_status(cls, db: Session, participant_id: str, current_user_id: str, new_status: MusterParticipantStatus, reason: str) -> MusterParticipantResponse:
        participant = db.query(MusterParticipant).filter(MusterParticipant.id == participant_id).first()
        if not participant:
            raise ValueError("Participant not found")

        old_status = participant.status
        if old_status == new_status:
            return cls._map_participant_to_dto(participant)

        participant.status = new_status
        participant.acknowledged_at = datetime.now(timezone.utc)
        participant.acknowledged_by = current_user_id

        audit_log = MusterAuditLog(
            participant_id=participant.id,
            old_status=old_status,
            new_status=new_status,
            performed_by=current_user_id,
            reason=reason
        )
        db.add(audit_log)
        db.commit()
        db.refresh(participant)
        return cls._map_participant_to_dto(participant)

    @classmethod
    def dashboard(cls, db: Session, session_id: str) -> MusterDashboard:
        session = db.query(MusterSession).filter(MusterSession.id == session_id).first()
        if not session:
            raise ValueError("Session not found")

        counts = db.query(
            MusterParticipant.status, 
            func.count(MusterParticipant.id)
        ).filter(
            MusterParticipant.muster_session_id == session_id
        ).group_by(MusterParticipant.status).all()

        counts_dict = {status: count for status, count in counts}

        safe_count = counts_dict.get(MusterParticipantStatus.SAFE, 0)
        missing_count = counts_dict.get(MusterParticipantStatus.MISSING, 0)
        unaccounted_count = counts_dict.get(MusterParticipantStatus.UNACCOUNTED, 0)
        manually_accounted_count = counts_dict.get(MusterParticipantStatus.MANUALLY_ACCOUNTED, 0)
        total_participants = sum(counts_dict.values())

        summary = MusterSummary(
            safe_count=safe_count,
            missing_count=missing_count,
            unaccounted_count=unaccounted_count,
            manually_accounted_count=manually_accounted_count,
            total_participants=total_participants
        )

        return MusterDashboard(
            session=cls._map_session_to_dto(session),
            summary=summary
        )
