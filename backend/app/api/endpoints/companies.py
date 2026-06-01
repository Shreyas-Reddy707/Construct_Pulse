from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Company, User, UserRole
from app.api.deps import get_current_user, RoleChecker

router = APIRouter()

@router.get("/", response_model=List[schemas.CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.post("/", response_model=schemas.CompanyResponse)
def create_company(
    company_in: schemas.CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    company = Company(**company_in.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
