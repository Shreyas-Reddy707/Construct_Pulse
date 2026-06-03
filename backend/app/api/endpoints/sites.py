from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone
import uuid
import math
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Site, User, Department, Contractor, SiteQRCode, UserRole
from app.api.deps import get_current_user, RoleChecker

router = APIRouter()

@router.get("/", response_model=List[schemas.SiteResponse])
def read_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Site)
    if current_user.company_id:
        query = query.filter(Site.company_id == current_user.company_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.SiteResponse)
def create_site(site_in: schemas.SiteCreate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site_data = site_in.model_dump()
    if current_user.company_id:
        site_data["company_id"] = current_user.company_id
    site = Site(**site_data)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site

@router.get("/{site_id}", response_model=schemas.SiteResponse)
def read_site(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        query = query.filter(Site.company_id == current_user.company_id)
    site = query.first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.put("/{site_id}", response_model=schemas.SiteResponse)
def update_site(site_id: str, site_in: schemas.SiteUpdate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    query = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        query = query.filter(Site.company_id == current_user.company_id)
    site = query.first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    update_data = site_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(site, key, value)
    
    db.commit()
    db.refresh(site)
    return site

@router.delete("/{site_id}")
def delete_site(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    query = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        query = query.filter(Site.company_id == current_user.company_id)
    site = query.first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    db.delete(site)
    db.commit()
    return {"ok": True}

# --- Site Assignments ---

@router.post("/{site_id}/assign-worker")
def assign_worker(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        site = site.filter(Site.company_id == current_user.company_id)
    site = site.first()
    
    user = db.query(User).filter(User.id == assignment.worker_id)
    if current_user.company_id:
        user = user.filter(User.company_id == current_user.company_id)
    user = user.first()
    
    if not site or not user:
        raise HTTPException(status_code=404, detail="Site or User not found")
        
    if user.role != UserRole.WORKER:
        raise HTTPException(status_code=400, detail="Only Worker accounts may be assigned to sites")
    site.assigned_workers.append(user)
    db.commit()
    return {"message": "Worker assigned successfully"}

@router.post("/{site_id}/assign-department")
def assign_department(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        site = site.filter(Site.company_id == current_user.company_id)
    site = site.first()
    
    dept = db.query(Department).filter(Department.id == assignment.department_id)
    if current_user.company_id:
        dept = dept.filter(Department.company_id == current_user.company_id)
    dept = dept.first()
    if not site or not dept:
        raise HTTPException(status_code=404, detail="Site or Department not found")
    site.assigned_departments.append(dept)
    db.commit()
    return {"message": "Department assigned successfully"}

@router.post("/{site_id}/assign-contractor")
def assign_contractor(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        site = site.filter(Site.company_id == current_user.company_id)
    site = site.first()
    
    contractor = db.query(Contractor).filter(Contractor.id == assignment.contractor_id)
    if current_user.company_id:
        contractor = contractor.filter(Contractor.company_id == current_user.company_id)
    contractor = contractor.first()
    if not site or not contractor:
        raise HTTPException(status_code=404, detail="Site or Contractor not found")
    site.assigned_contractors.append(contractor)
    db.commit()
    return {"message": "Contractor assigned successfully"}

@router.get("/{site_id}/assignments", response_model=schemas.SiteAssignmentsResponse)
def get_assignments(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id)
    if current_user.company_id:
        site = site.filter(Site.company_id == current_user.company_id)
    site = site.first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return {
        "workers": [u.id for u in site.assigned_workers],
        "departments": [d.id for d in site.assigned_departments],
        "contractors": [c.id for c in site.assigned_contractors]
    }

# --- QR Management ---

@router.post("/{site_id}/generate-qr", response_model=schemas.QRCodeResponse)
def generate_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Check existing valid QR
    existing_qr = db.query(SiteQRCode).filter(SiteQRCode.site_id == site_id, SiteQRCode.expires_at > datetime.now(timezone.utc)).first()
    if existing_qr:
        return existing_qr

    new_qr = SiteQRCode(
        site_id=site_id,
        qr_token=str(uuid.uuid4()),
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)
    return new_qr

@router.post("/{site_id}/refresh-qr", response_model=schemas.QRCodeResponse)
def refresh_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Invalidate old ones
    db.query(SiteQRCode).filter(SiteQRCode.site_id == site_id).update({"expires_at": datetime.now(timezone.utc)})
    
    new_qr = SiteQRCode(
        site_id=site_id,
        qr_token=str(uuid.uuid4()),
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)
    return new_qr

@router.get("/{site_id}/qr", response_model=schemas.QRCodeResponse)
def get_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    qr = db.query(SiteQRCode).filter(SiteQRCode.site_id == site_id, SiteQRCode.expires_at > datetime.now(timezone.utc)).order_by(SiteQRCode.created_at.desc()).first()
    if not qr:
        raise HTTPException(status_code=404, detail="Active QR not found")
    return qr
