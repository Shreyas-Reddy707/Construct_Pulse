from fastapi import APIRouter, Depends
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
