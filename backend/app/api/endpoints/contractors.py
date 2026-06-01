from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Contractor, User, UserRole
from app.api.deps import get_current_user, RoleChecker

router = APIRouter()

@router.get("/", response_model=List[schemas.ContractorResponse])
def read_contractors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contractors = db.query(Contractor).offset(skip).limit(limit).all()
    return contractors

@router.post("/", response_model=schemas.ContractorResponse)
def create_contractor(
    contractor_in: schemas.ContractorCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    contractor = Contractor(**contractor_in.model_dump())
    db.add(contractor)
    db.commit()
    db.refresh(contractor)
    return contractor
