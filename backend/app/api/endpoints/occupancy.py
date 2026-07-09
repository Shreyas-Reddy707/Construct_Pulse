from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User
from app.api.deps import get_current_user, PermissionChecker
from app.services.occupancy_service import OccupancyService

router = APIRouter()

@router.post("/dashboard", response_model=schemas.OccupancyDashboard)
def get_dashboard(
    query: schemas.OccupancyQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Returns an aggregated dashboard projection of current site occupancy.
    """
    return OccupancyService.get_dashboard(db, query, current_user)

@router.post("/muster", response_model=List[schemas.OccupancyWorker])
def get_muster_list(
    query: schemas.OccupancyQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Returns a paginated list of workers currently occupying a site.
    """
    return OccupancyService.get_muster_list(db, query, current_user)

@router.post("/snapshots/{site_id}", response_model=schemas.OccupancySnapshotResponse)
def capture_snapshot(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("attendance.view"))
):
    """
    Manually captures an occupancy snapshot for historical tracking.
    """
    return OccupancyService.capture_snapshot(db, site_id, current_user)

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
    return OccupancyService.list_snapshots(db, site_id, current_user, skip, limit)
