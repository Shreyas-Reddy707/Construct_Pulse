from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Company, User, UserRole
from app.api.deps import get_current_user, RoleChecker

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
    if company_in.registration_number:
        existing = db.query(Company).filter(Company.registration_number == company_in.registration_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Registration number already exists")
            
    company = Company(**company_in.model_dump())
    db.add(company)
    db.commit()
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
    target_user = db.query(User).filter(User.id == user_id, User.company_id == company_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found in this company")
        
    if target_user.role == UserRole.SYSTEM_ADMIN:
        raise HTTPException(status_code=400, detail="Cannot assign SYSTEM_ADMIN as COMPANY_ADMIN")
        
    target_user.role = UserRole.COMPANY_ADMIN
    target_user.status = "approved"
    target_user.is_active = True
    
    db.commit()
    db.refresh(target_user)
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"SYSTEM_ADMIN {current_user.id} assigned COMPANY_ADMIN {target_user.id} to company {company_id}")
    
    return target_user
