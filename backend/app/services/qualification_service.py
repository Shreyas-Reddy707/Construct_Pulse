from sqlalchemy.orm import Session
from app.models.models import WorkerQualification, QualificationType, VerificationStatus, User
from app.schemas.schemas import WorkerQualificationCreate
from fastapi import HTTPException
from datetime import datetime, timezone

class QualificationService:
    @classmethod
    def create_worker_qualification(cls, db: Session, worker_id: str, qual_in: WorkerQualificationCreate) -> WorkerQualification:
        # Reject duplicate active qualifications for the same worker and qualification type
        existing = db.query(WorkerQualification).filter(
            WorkerQualification.worker_id == worker_id,
            WorkerQualification.qualification_type_id == qual_in.qualification_type_id,
            WorkerQualification.is_deleted == False
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Worker already has an active qualification of this type.")

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
    def get_worker_qualifications(cls, db: Session, worker_id: str):
        return db.query(WorkerQualification).filter(
            WorkerQualification.worker_id == worker_id,
            WorkerQualification.is_deleted == False
        ).all()

    @classmethod
    def get_qualification(cls, db: Session, qual_id: str) -> WorkerQualification:
        qual = db.query(WorkerQualification).filter(
            WorkerQualification.id == qual_id,
            WorkerQualification.is_deleted == False
        ).first()
        if not qual:
            raise HTTPException(status_code=404, detail="Qualification not found.")
        return qual

    @classmethod
    def update_verification_status(cls, db: Session, qual_id: str, status: VerificationStatus) -> WorkerQualification:
        qual = cls.get_qualification(db, qual_id)
        qual.verification_status = status
        db.commit()
        db.refresh(qual)
        return qual

    @classmethod
    def remove_qualification(cls, db: Session, qual_id: str):
        qual = cls.get_qualification(db, qual_id)
        qual.is_deleted = True
        qual.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return {"message": "Qualification removed successfully."}

    @classmethod
    def get_compliance_passport(cls, db: Session, worker_id: str):
        worker = db.query(User).filter(User.id == worker_id, User.is_deleted == False).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found.")
            
        from app.services.worker_readiness_service import WorkerReadinessService
        readiness = WorkerReadinessService.evaluate(worker)
        
        qualifications = cls.get_worker_qualifications(db, worker_id)
        
        return {
            "worker_id": worker_id,
            "ready": readiness.get("ready", False),
            "missing_requirements": readiness.get("missing", []),
            "qualifications": qualifications
        }
