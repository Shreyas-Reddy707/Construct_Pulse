from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.schemas import (
    ConfigurationDraftRequest, ConfigurationApproveRequest, ConfigurationResponse,
    ConfigurationVersionResponse, ConfigurationDashboard
)
from app.services.configuration_service import PlatformConfigurationService
from app.models.models import User

router = APIRouter()

@router.post("/draft", response_model=ConfigurationResponse, status_code=status.HTTP_201_CREATED)
def draft_configuration(
    payload: ConfigurationDraftRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return PlatformConfigurationService.create_draft(
            db=db,
            company_id=current_user.company_id,
            current_user_id=current_user.id,
            payload=payload
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{version_id}/approve", response_model=ConfigurationResponse)
def approve_configuration(
    version_id: str,
    payload: ConfigurationApproveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return PlatformConfigurationService.approve(
            db=db,
            version_id=version_id,
            current_user_id=current_user.id,
            payload=payload
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ConfigurationResponse])
def list_configurations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return PlatformConfigurationService.list_configurations(
            db=db,
            company_id=current_user.company_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{config_key}/history", response_model=List[ConfigurationVersionResponse])
def get_configuration_history(
    config_key: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return PlatformConfigurationService.get_configuration_history(
            db=db,
            company_id=current_user.company_id,
            config_key=config_key
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard", response_model=ConfigurationDashboard)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return PlatformConfigurationService.dashboard(
            db=db,
            company_id=current_user.company_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
