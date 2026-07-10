from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole
from app.api.deps import get_current_user, RoleChecker, PermissionChecker
from app.services.site_service import SiteService
from app.modules.sites.services.site_workspace_service import SiteWorkspaceService
from app.modules.sites.schemas.site_dto import SiteDetailResponse

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse[schemas.SiteResponse])
def read_sites(
    query: schemas.SiteQuery = Depends(), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    items, total = SiteService.get_sites(db, current_user, query)
    return schemas.PaginatedResponse.create(data=items, total_records=total, skip=query.skip, limit=query.limit)

@router.post("/", response_model=schemas.SiteResponse)
def create_site(site_in: schemas.SiteCreate, db: Session = Depends(get_db), current_user: User = Depends(PermissionChecker("site.create"))):
    site = SiteService.create_site(db, current_user, site_in)
    db.refresh(site)
    return site

@router.get("/{site_id}", response_model=schemas.SiteResponse)
def read_site(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return SiteService.get_site(db, site_id, current_user)

@router.get("/{site_id}/workspace", response_model=SiteDetailResponse)
def read_site_workspace(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return SiteWorkspaceService.get_site_workspace_detail(db, site_id, current_user)


@router.put("/{site_id}", response_model=schemas.SiteResponse)
def update_site(site_id: str, site_in: schemas.SiteUpdate, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.update_site(db, site_id, current_user, site_in)

@router.delete("/{site_id}")
def delete_site(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    SiteService.delete_site(db, site_id, current_user)
    return {"ok": True}

@router.post("/{site_id}/activate")
def activate_site(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.activate_site(db, site_id, current_user)

@router.post("/{site_id}/suspend", response_model=schemas.SiteResponse)
def suspend_site(site_id: str, request: schemas.SiteSuspendRequest, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.suspend_site(db, site_id, current_user, request)

# --- Site Assignments ---

@router.post("/{site_id}/assign-worker")
def assign_worker(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    SiteService.assign_worker(db, site_id, current_user, assignment)
    return {"message": "Worker assigned successfully"}

@router.delete("/{site_id}/unassign-worker/{worker_id}")
def unassign_worker(site_id: str, worker_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    SiteService.unassign_worker(db, site_id, worker_id, current_user)
    return {"message": "Worker unassigned successfully"}

@router.post("/{site_id}/assign-department")
def assign_department(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    SiteService.assign_department(db, site_id, current_user, assignment)
    return {"message": "Department assigned successfully"}

@router.post("/{site_id}/assign-contractor")
def assign_contractor(site_id: str, assignment: schemas.SiteAssignment, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    SiteService.assign_contractor(db, site_id, current_user, assignment)
    return {"message": "Contractor assigned successfully"}

@router.get("/{site_id}/assignments", response_model=schemas.SiteAssignmentsResponse)
def get_assignments(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.get_assignments(db, site_id, current_user)

# --- QR Management ---

@router.post("/{site_id}/generate-qr", response_model=schemas.QRCodeResponse)
def generate_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.generate_qr(db, site_id, current_user)

@router.post("/{site_id}/refresh-qr", response_model=schemas.QRCodeResponse)
def refresh_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.refresh_qr(db, site_id, current_user)

@router.get("/{site_id}/qr", response_model=schemas.QRCodeResponse)
def get_qr(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))):
    return SiteService.get_qr(db, site_id, current_user)
