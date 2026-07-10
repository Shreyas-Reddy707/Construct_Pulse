from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole
from app.api.deps import get_current_user, RoleChecker
from app.services.contractor_service import ContractorService
from app.modules.contractors.services.contractor_workspace_service import ContractorWorkspaceService
from app.modules.contractors.schemas.contractor_dto import ContractorDetailResponse

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse[schemas.ContractorResponse])
def read_contractors(
    query: schemas.ContractorQuery = Depends(), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    items, total = ContractorService.get_contractors(db, current_user, query)
    return schemas.PaginatedResponse.create(data=items, total_records=total, skip=query.skip, limit=query.limit)

@router.post("/", response_model=schemas.ContractorResponse)
def create_contractor(
    contractor_in: schemas.ContractorCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    contractor = ContractorService.create_contractor(db, current_user, contractor_in)
    db.refresh(contractor)
    return contractor

@router.get("/{contractor_id}/workspace", response_model=ContractorDetailResponse)
def read_contractor_workspace(
    contractor_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return ContractorWorkspaceService.get_contractor_workspace_detail(db, contractor_id, current_user)
