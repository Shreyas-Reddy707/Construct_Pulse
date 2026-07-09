from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.api.deps import PermissionChecker
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports.view"))
):
    """
    Returns a lightweight payload of highly aggregated KPI metrics for dashboard summary cards.
    """
    return AnalyticsService.get_summary(db, current_user)

@router.get("/trends")
def get_dashboard_trends(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    site_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports.view"))
):
    """
    Returns a flat chronological array of daily KPIs (headcount, hours, corrections) 
    designed specifically for direct binding to React charting libraries.
    """
    return AnalyticsService.get_daily_trends(
        session=db,
        current_user=current_user,
        start_date=start_date,
        end_date=end_date,
        site_id=site_id
    )
