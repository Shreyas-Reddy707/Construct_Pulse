from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, PermissionChecker
from app.models.models import User
from app.schemas import schemas
from app.services.notification_service import NotificationService

router = APIRouter()

@router.post("", response_model=schemas.NotificationResponse)
def create_notification(
    payload: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("notifications.manage"))
):
    """
    Creates a new notification. Manager access required.
    """
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User must belong to a company")
    try:
        return NotificationService.create_notification(db, current_user.company_id, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.NotificationResponse])
def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lists notifications where the current user is a recipient.
    """
    return NotificationService.list_notifications(db, current_user.id, skip, limit)

@router.get("/dashboard", response_model=schemas.NotificationDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets dashboard summary of notifications for the current user.
    """
    return NotificationService.dashboard(db, current_user.id)

@router.get("/{notification_id}", response_model=schemas.NotificationResponse)
def get_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gets details of a specific notification for the recipient.
    """
    notification = NotificationService.get_notification(db, notification_id, current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/{notification_id}/read", response_model=schemas.NotificationResponse)
def mark_read(
    notification_id: str,
    payload: schemas.NotificationReadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marks a notification as READ for the recipient.
    """
    try:
        return NotificationService.mark_read(db, notification_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{notification_id}/archive", response_model=schemas.NotificationResponse)
def archive_notification(
    notification_id: str,
    payload: schemas.NotificationArchiveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marks a notification as ARCHIVED for the recipient.
    """
    try:
        return NotificationService.archive(db, notification_id, current_user.id, payload.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
