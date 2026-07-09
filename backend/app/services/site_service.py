from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.models import Site, User, Department, Contractor, SiteQRCode, UserRole, SiteStatus, WorkerStatus
from app.schemas import schemas
from app.core.exceptions import ResourceNotFoundException, ValidationException, StateTransitionException
from app.services.site_readiness_service import SiteReadinessService
from datetime import datetime, timedelta, timezone
import uuid
import math
from typing import List

class SiteService:
    @classmethod
    def get_sites(cls, db: Session, current_user: User, skip: int = 0, limit: int = 100) -> List[Site]:
        query = db.query(Site)
        if current_user.role == UserRole.WORKER:
            query = query.filter(Site.assigned_workers.any(User.id == current_user.id))
        elif current_user.company_id:
            query = query.filter(Site.company_id == current_user.company_id)
        return query.offset(skip).limit(limit).all()

    @classmethod
    def get_site(cls, db: Session, site_id: str, current_user: User) -> Site:
        query = db.query(Site).filter(Site.id == site_id)
        if current_user.company_id:
            query = query.filter(Site.company_id == current_user.company_id)
        site = query.first()
        if not site:
            raise ResourceNotFoundException("Site not found")
        return site

    @classmethod
    def create_site(cls, db: Session, current_user: User, site_in: schemas.SiteCreate) -> Site:
        site_data = site_in.model_dump()
        if current_user.company_id:
            site_data["company_id"] = current_user.company_id
        site = Site(**site_data)
        db.add(site)
        return site

    @classmethod
    def update_site(cls, db: Session, site_id: str, current_user: User, site_in: schemas.SiteUpdate) -> Site:
        site = cls.get_site(db, site_id, current_user)
        update_data = site_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(site, key, value)
        db.refresh(site)
        SiteReadinessService.update_lifecycle_state(site, db)
        return site

    @classmethod
    def delete_site(cls, db: Session, site_id: str, current_user: User) -> None:
        site = cls.get_site(db, site_id, current_user)
        site.is_deleted = True
        site.deleted_at = datetime.now(timezone.utc)
        site.status = SiteStatus.ARCHIVED

    @classmethod
    def activate_site(cls, db: Session, site_id: str, current_user: User) -> Site:
        site = cls.get_site(db, site_id, current_user)
        if site.status == SiteStatus.ARCHIVED:
            raise StateTransitionException("Cannot activate an archived site")
            
        readiness = SiteReadinessService.evaluate(site, db)
        if not readiness["ready"]:
            # Rather than returning JSONResponse (which leaks presentation into service layer), 
            # we should raise an exception that the global handler formats, but to preserve existing exactly:
            # We raise a BusinessRuleViolation with a specific message, or we can just raise ValidationException.
            raise ValidationException("Site is not ready for activation. Missing: " + ", ".join(readiness["missing"]))
            
        site.status = SiteStatus.ACTIVE
        site.activated_by = current_user.id
        site.activated_at = datetime.now(timezone.utc)
        db.refresh(site)
        return site

    @classmethod
    def suspend_site(cls, db: Session, site_id: str, current_user: User, request: schemas.SiteSuspendRequest) -> Site:
        site = cls.get_site(db, site_id, current_user)
        if site.status == SiteStatus.ARCHIVED:
            raise StateTransitionException("Cannot suspend an archived site")
            
        site.status = SiteStatus.SUSPENDED
        if request and request.reason:
            site.suspension_reason = request.reason
        db.refresh(site)
        return site

    @classmethod
    def assign_worker(cls, db: Session, site_id: str, current_user: User, assignment: schemas.SiteAssignment) -> None:
        site = cls.get_site(db, site_id, current_user)
        
        user = db.query(User).filter(User.id == assignment.worker_id)
        if current_user.company_id:
            user = user.filter(User.company_id == current_user.company_id)
        user = user.first()
        
        if not user:
            raise ResourceNotFoundException("Site or User not found")
            
        if getattr(user, "is_deleted", False):
            raise ValidationException("Archived workers cannot be assigned")
            
        if user.status == WorkerStatus.SUSPENDED:
            raise ValidationException("Suspended workers cannot be assigned")
            
        if site.status == SiteStatus.ARCHIVED:
            raise StateTransitionException("Cannot assign worker to an archived site")
            
        if user.role != UserRole.WORKER:
            raise ValidationException("Only Worker accounts may be assigned to sites")
            
        site.assigned_workers.append(user)
        SiteReadinessService.update_lifecycle_state(site, db)

    @classmethod
    def unassign_worker(cls, db: Session, site_id: str, worker_id: str, current_user: User) -> None:
        site = cls.get_site(db, site_id, current_user)
        user = next((u for u in site.assigned_workers if str(u.id) == worker_id), None)
        if not user:
            raise ResourceNotFoundException("Worker not assigned to this site")
            
        site.assigned_workers.remove(user)
        SiteReadinessService.update_lifecycle_state(site, db)

    @classmethod
    def assign_department(cls, db: Session, site_id: str, current_user: User, assignment: schemas.SiteAssignment) -> None:
        site = cls.get_site(db, site_id, current_user)
        
        dept = db.query(Department).filter(Department.id == assignment.department_id)
        if current_user.company_id:
            dept = dept.filter(Department.company_id == current_user.company_id)
        dept = dept.first()
        if not dept:
            raise ResourceNotFoundException("Site or Department not found")
            
        site.assigned_departments.append(dept)

    @classmethod
    def assign_contractor(cls, db: Session, site_id: str, current_user: User, assignment: schemas.SiteAssignment) -> None:
        site = cls.get_site(db, site_id, current_user)
        
        contractor = db.query(Contractor).filter(Contractor.id == assignment.contractor_id)
        if current_user.company_id:
            contractor = contractor.filter(Contractor.company_id == current_user.company_id)
        contractor = contractor.first()
        if not contractor:
            raise ResourceNotFoundException("Site or Contractor not found")
            
        site.assigned_contractors.append(contractor)

    @classmethod
    def get_assignments(cls, db: Session, site_id: str, current_user: User) -> dict:
        site = cls.get_site(db, site_id, current_user)
        return {
            "workers": site.assigned_workers,
            "departments": site.assigned_departments,
            "contractors": site.assigned_contractors
        }

    @classmethod
    def generate_qr(cls, db: Session, site_id: str, current_user: User) -> SiteQRCode:
        site = cls.get_site(db, site_id, current_user)
        now_utc = datetime.now(timezone.utc)

        active_qrs = db.query(SiteQRCode).filter(
            SiteQRCode.site_id == site_id,
            or_(SiteQRCode.expires_at == None, SiteQRCode.expires_at > now_utc)
        ).all()
        
        if len(active_qrs) == 1:
            return active_qrs[0]
        
        db.query(SiteQRCode).filter(
            SiteQRCode.site_id == site_id,
            or_(SiteQRCode.expires_at == None, SiteQRCode.expires_at > now_utc)
        ).update({"expires_at": now_utc}, synchronize_session=False)

        new_qr = SiteQRCode(
            site_id=site_id,
            qr_token=str(uuid.uuid4()),
            expires_at=now_utc + timedelta(days=365)
        )
        db.add(new_qr)
        db.refresh(new_qr)
        SiteReadinessService.update_lifecycle_state(site, db)
        return new_qr

    @classmethod
    def refresh_qr(cls, db: Session, site_id: str, current_user: User) -> SiteQRCode:
        site = cls.get_site(db, site_id, current_user)
        now_utc = datetime.now(timezone.utc)

        db.query(SiteQRCode).filter(
            SiteQRCode.site_id == site_id,
            or_(SiteQRCode.expires_at == None, SiteQRCode.expires_at > now_utc)
        ).update({"expires_at": now_utc}, synchronize_session=False)
        
        new_qr = SiteQRCode(
            site_id=site_id,
            qr_token=str(uuid.uuid4()),
            expires_at=now_utc + timedelta(days=365)
        )
        db.add(new_qr)
        db.refresh(new_qr)
        SiteReadinessService.update_lifecycle_state(site, db)
        return new_qr

    @classmethod
    def get_qr(cls, db: Session, site_id: str, current_user: User) -> SiteQRCode:
        site = cls.get_site(db, site_id, current_user)
        now_utc = datetime.now(timezone.utc)
        
        qr = db.query(SiteQRCode).filter(
            SiteQRCode.site_id == site_id, 
            or_(SiteQRCode.expires_at == None, SiteQRCode.expires_at > now_utc)
        ).order_by(SiteQRCode.created_at.desc()).first()
        
        if not qr:
            raise ResourceNotFoundException("Active QR not found")
        return qr
