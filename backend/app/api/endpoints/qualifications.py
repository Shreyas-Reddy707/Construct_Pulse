from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.schemas import WorkerQualificationCreate, WorkerQualificationResponse, WorkerQualificationUpdate, CompliancePassportResponse
from app.services.qualification_service import QualificationService
from app.models.models import VerificationStatus

router = APIRouter()

@router.post("/workers/{worker_id}/qualifications", response_model=WorkerQualificationResponse)
def upload_qualification(
    worker_id: str, 
    qual_in: WorkerQualificationCreate, 
    db: Session = Depends(get_db)
):
    """
    Upload a new qualification for a worker.
    """
    return QualificationService.create_worker_qualification(db, worker_id, qual_in)

@router.get("/workers/{worker_id}/qualifications", response_model=List[WorkerQualificationResponse])
def list_worker_qualifications(
    worker_id: str, 
    db: Session = Depends(get_db)
):
    """
    List all active qualifications for a worker.
    """
    return QualificationService.get_worker_qualifications(db, worker_id)

@router.get("/qualifications/{qual_id}", response_model=WorkerQualificationResponse)
def view_qualification(
    qual_id: str, 
    db: Session = Depends(get_db)
):
    """
    View details of a specific qualification.
    """
    return QualificationService.get_qualification(db, qual_id)

@router.patch("/qualifications/{qual_id}/verification", response_model=WorkerQualificationResponse)
def update_verification_status(
    qual_id: str, 
    status_update: WorkerQualificationUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update the verification status of a qualification.
    """
    return QualificationService.update_verification_status(db, qual_id, VerificationStatus(status_update.verification_status))

@router.delete("/qualifications/{qual_id}")
def remove_qualification(
    qual_id: str, 
    db: Session = Depends(get_db)
):
    """
    Soft-delete a qualification.
    """
    return QualificationService.remove_qualification(db, qual_id)

@router.get("/compliance/passport/{worker_id}", response_model=CompliancePassportResponse)
def get_compliance_passport(
    worker_id: str, 
    db: Session = Depends(get_db)
):
    """
    Get the dynamic compliance passport for a worker.
    """
    return QualificationService.get_compliance_passport(db, worker_id)
