from sqlalchemy.orm import Session
from app.models.models import WorkerQualification, QualificationType, VerificationStatus, User
from app.schemas.schemas import WorkerQualificationCreate
from datetime import datetime, timezone

class QualificationService:
    @classmethod
    def _get_worker_for_tenant(cls, db: Session, worker_id: str, current_user: User) -> User:
        from app.models.models import UserRole
        query = db.query(User).filter(User.id == worker_id, User.is_deleted == False)
        
        if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
            query = query.filter(User.company_id == current_user.company_id)
            
        worker = query.first()
        if not worker:
            from app.core.exceptions import ResourceNotFoundException
            raise ResourceNotFoundException("Worker not found or access denied")
        return worker

    @classmethod
    def _get_qualification_for_tenant(cls, db: Session, qual_id: str, current_user: User) -> WorkerQualification:
        from app.models.models import UserRole
        query = db.query(WorkerQualification).join(User).filter(
            WorkerQualification.id == qual_id,
            WorkerQualification.is_deleted == False
        )
        
        if current_user.company_id and current_user.role != UserRole.SYSTEM_ADMIN:
            query = query.filter(User.company_id == current_user.company_id)
            
        qual = query.first()
        if not qual:
            from app.core.exceptions import ResourceNotFoundException
            raise ResourceNotFoundException("Qualification not found or access denied")
        return qual

    @classmethod
    def create_worker_qualification(cls, db: Session, worker_id: str, qual_in: WorkerQualificationCreate, current_user: User) -> WorkerQualification:
        cls._get_worker_for_tenant(db, worker_id, current_user)

        # Reject duplicate active qualifications for the same worker and qualification type
        existing = db.query(WorkerQualification).filter(
            WorkerQualification.worker_id == worker_id,
            WorkerQualification.qualification_type_id == qual_in.qualification_type_id,
            WorkerQualification.is_deleted == False
        ).first()

        if existing:
            from app.core.exceptions import ConflictException
            raise ConflictException("Worker already has an active qualification of this type.")

        new_qual = WorkerQualification(
            worker_id=worker_id,
            qualification_type_id=qual_in.qualification_type_id,
            certificate_number=qual_in.certificate_number,
            issuing_authority=qual_in.issuing_authority,
            issue_date=qual_in.issue_date,
            expiry_date=qual_in.expiry_date,
            document_url=qual_in.document_url,
            verification_status=VerificationStatus.PENDING
        )
        db.add(new_qual)
        db.commit()
        db.refresh(new_qual)
        return new_qual

    @classmethod
    def get_worker_qualifications(cls, db: Session, worker_id: str, current_user: User):
        cls._get_worker_for_tenant(db, worker_id, current_user)
        return db.query(WorkerQualification).filter(
            WorkerQualification.worker_id == worker_id,
            WorkerQualification.is_deleted == False
        ).all()

    @classmethod
    def get_qualification(cls, db: Session, qual_id: str, current_user: User) -> WorkerQualification:
        return cls._get_qualification_for_tenant(db, qual_id, current_user)

    @classmethod
    def update_verification_status(cls, db: Session, qual_id: str, status: VerificationStatus, current_user: User) -> WorkerQualification:
        qual = cls._get_qualification_for_tenant(db, qual_id, current_user)
        qual.verification_status = status
        db.commit()
        db.refresh(qual)
        return qual

    @classmethod
    def remove_qualification(cls, db: Session, qual_id: str, current_user: User):
        qual = cls._get_qualification_for_tenant(db, qual_id, current_user)
        qual.is_deleted = True
        qual.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return {"message": "Qualification removed successfully."}

    @classmethod
    def get_compliance_passport(cls, db: Session, worker_id: str, current_user: User):
        worker = cls._get_worker_for_tenant(db, worker_id, current_user)
            
        from app.services.worker_readiness_service import WorkerReadinessService
        readiness = WorkerReadinessService.evaluate(worker)
        
        qualifications = cls.get_worker_qualifications(db, worker_id, current_user)
        
        return {
            "worker_id": worker_id,
            "ready": readiness.get("ready", False),
            "missing_requirements": readiness.get("missing", []),
            "qualifications": qualifications
        }
