from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from app.db.database import get_db
from app.models.models import User, Site, InductionPackage, WorkerInductionRecord, UserRole
from app.schemas import schemas
from app.api.deps import get_current_user, RoleChecker
from pydantic import BaseModel

router = APIRouter()

class InductionPackageResponse(BaseModel):
    id: str
    site_id: str
    version: int
    title: str
    is_active: bool
    expiry_days: int
    quiz_enabled: bool

    class Config:
        from_attributes = True

class InductionRecordResponse(BaseModel):
    id: str
    worker_id: str
    package_id: str
    completed_at: datetime
    expires_at: datetime
    worker_acknowledgement: bool
    package_version_completed: int

    class Config:
        from_attributes = True

class InductionAcknowledgementRequest(BaseModel):
    worker_acknowledgement: bool

@router.get("/sites/{site_id}/induction", response_model=InductionPackageResponse)
def get_site_induction_package(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the active induction package for a specific site.
    """
    # Verify the site exists and is active
    site = db.query(Site).filter(Site.id == site_id, Site.status == "active").first()
    if not site:
        raise HTTPException(status_code=404, detail="Active site not found")

    # Verify the user is assigned to the site (or is an admin)
    if current_user.role == UserRole.WORKER:
        is_assigned = any(str(s.id) == site_id for s in current_user.assigned_sites)
        if not is_assigned:
            raise HTTPException(status_code=403, detail="Not assigned to this site")
    elif current_user.company_id and current_user.company_id != site.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this site's induction")

    # Fetch the active induction package for the site
    package = db.query(InductionPackage).filter(
        InductionPackage.site_id == site_id,
        InductionPackage.is_active == True
    ).order_by(InductionPackage.version.desc()).first()

    if not package:
        raise HTTPException(status_code=404, detail="No active induction package found for this site")

    return package

@router.post("/sites/{site_id}/induction/acknowledge", response_model=InductionRecordResponse)
def acknowledge_site_induction(
    site_id: str,
    request: InductionAcknowledgementRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.WORKER]))
):
    """
    Submit a worker acknowledgement and complete the induction for the active package.
    """
    if not request.worker_acknowledgement:
        raise HTTPException(status_code=400, detail="Worker must explicitly acknowledge the induction")

    # Verify the site exists and is active
    site = db.query(Site).filter(Site.id == site_id, Site.status == "active").first()
    if not site:
        raise HTTPException(status_code=404, detail="Active site not found")

    # Verify the worker is assigned to the site
    is_assigned = any(str(s.id) == site_id for s in current_user.assigned_sites)
    if not is_assigned:
        raise HTTPException(status_code=403, detail="Not assigned to this site")

    # Fetch the active induction package
    package = db.query(InductionPackage).filter(
        InductionPackage.site_id == site_id,
        InductionPackage.is_active == True
    ).order_by(InductionPackage.version.desc()).first()

    if not package:
        raise HTTPException(status_code=404, detail="No active induction package found for this site")

    # Calculate expiry
    now_utc = datetime.now(timezone.utc)
    expires_at = now_utc + timedelta(days=package.expiry_days)

    # Check if a record for this package already exists
    record = db.query(WorkerInductionRecord).filter(
        WorkerInductionRecord.worker_id == current_user.id,
        WorkerInductionRecord.package_id == package.id
    ).first()

    if record:
        # Update existing record
        record.completed_at = now_utc
        record.expires_at = expires_at
        record.worker_acknowledgement = True
        record.package_version_completed = package.version
    else:
        # Create new record
        record = WorkerInductionRecord(
            worker_id=current_user.id,
            package_id=package.id,
            completed_at=now_utc,
            expires_at=expires_at,
            worker_acknowledgement=True,
            package_version_completed=package.version
        )
        db.add(record)

    db.commit()
    db.refresh(record)

    return record

@router.get("/users/{user_id}/induction-status", response_model=List[InductionRecordResponse])
def get_worker_induction_status(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve the worker's induction status/records.
    """
    # Verify authorization
    if current_user.role == UserRole.WORKER and str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view another worker's induction status")
    
    worker = db.query(User).filter(User.id == user_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
        
    if current_user.company_id and current_user.role != UserRole.WORKER:
        if worker.company_id != current_user.company_id:
            raise HTTPException(status_code=403, detail="Worker does not belong to your company")

    records = db.query(WorkerInductionRecord).filter(
        WorkerInductionRecord.worker_id == user_id
    ).all()

    return records
