from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Company, User, UserRole
from app.api.deps import get_current_user, RoleChecker
from app.services.company_service import CompanyService

router = APIRouter()

@router.get("/", response_model=List[schemas.CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(RoleChecker([UserRole.SYSTEM_ADMIN]))):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.post("/", response_model=schemas.CompanyResponse)
def create_company(
    company_in: schemas.CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.SYSTEM_ADMIN]))
):
    company = CompanyService.create_company(db, company_in)
    db.refresh(company)
    return company

@router.get("/{company_id}/users", response_model=List[schemas.UserResponse])
def get_company_users(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.SYSTEM_ADMIN]))
):
    users = db.query(User).filter(User.company_id == company_id).all()
    return users

@router.put("/{company_id}/assign-admin/{user_id}", response_model=schemas.UserResponse)
def assign_company_admin(
    company_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.SYSTEM_ADMIN]))
):
    target_user = CompanyService.assign_company_admin(db, company_id, user_id, current_user)
    db.refresh(target_user)
    return target_user
