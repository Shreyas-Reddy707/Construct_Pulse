from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole
from app.api.deps import get_current_user, RoleChecker
from app.services.contractor_service import ContractorService

router = APIRouter()

@router.get("/", response_model=List[schemas.ContractorResponse])
def read_contractors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ContractorService.get_contractors(db, current_user, skip, limit)

@router.post("/", response_model=schemas.ContractorResponse)
def create_contractor(
    contractor_in: schemas.ContractorCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    contractor = ContractorService.create_contractor(db, current_user, contractor_in)
    db.refresh(contractor)
    return contractor
