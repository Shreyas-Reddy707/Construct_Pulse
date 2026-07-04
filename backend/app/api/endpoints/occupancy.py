from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole, Site
from app.api.deps import get_current_user, PermissionChecker
from app.services.occupancy_service import OccupancyService

router = APIRouter()

def _enforce_tenant_isolation(current_user: User, query: schemas.OccupancyQuery, db: Session) -> schemas.OccupancyQuery:
    if current_user.role == UserRole.COMPANY_ADMIN:
        # Currently the query object doesn't have company_id, 
        # but we must ensure the requested site belongs to their company.
        if query.site_id:
            site = db.query(Site).filter(Site.id == query.site_id, Site.company_id == current_user.company_id).first()
            if not site:
                raise HTTPException(status_code=404, detail="Site not found")
        else:
            # We must lock the query to their company if they don't provide a site_id.
            # But the OccupancyQuery only filters by site_id.
            # Let's enforce that site_id is required for Company Admins for now.
            raise HTTPException(status_code=400, detail="site_id is required")
            
    elif current_user.role == UserRole.SITE_MANAGER:
        # Same logic for site managers for now
        if not query.site_id:
             raise HTTPException(status_code=400, detail="site_id is required")
             
        # Validate they have access to this site
        valid_site = any(s.id == query.site_id for s in current_user.assigned_sites)
        if not valid_site:
             raise HTTPException(status_code=403, detail="Not assigned to this site")
             
    elif current_user.role == UserRole.WORKER:
        raise HTTPException(status_code=403, detail="Workers cannot access occupancy data")
        
    return query

@router.post("/dashboard", response_model=schemas.OccupancyDashboard)
def get_dashboard(
    query: schemas.OccupancyQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Returns an aggregated dashboard projection of current site occupancy.
    """
    query = _enforce_tenant_isolation(current_user, query, db)
    return OccupancyService.get_dashboard(db, query)

@router.post("/muster", response_model=List[schemas.OccupancyWorker])
def get_muster_list(
    query: schemas.OccupancyQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Returns a paginated list of workers currently occupying a site.
    """
    query = _enforce_tenant_isolation(current_user, query, db)
    return OccupancyService.get_muster_list(db, query)

@router.post("/snapshots/{site_id}", response_model=schemas.OccupancySnapshotResponse)
def capture_snapshot(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Manually captures an occupancy snapshot for historical tracking.
    """
    query = schemas.OccupancyQuery(site_id=site_id)
    _enforce_tenant_isolation(current_user, query, db)
    return OccupancyService.capture_snapshot(db, site_id, captured_by=current_user.id)

@router.get("/snapshots/{site_id}", response_model=List[schemas.OccupancySnapshotResponse])
def list_snapshots(
    site_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Lists historical occupancy snapshots for a site.
    """
    query = schemas.OccupancyQuery(site_id=site_id)
    _enforce_tenant_isolation(current_user, query, db)
    
    return OccupancyService.list_snapshots(db, site_id, skip, limit)
