from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Department, Contractor, Company

router = APIRouter()

@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def read_public_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Publicly accessible endpoint to retrieve departments for user registration.
    """
    return db.query(Department).offset(skip).limit(limit).all()

@router.get("/contractors", response_model=List[schemas.ContractorResponse])
def read_public_contractors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Publicly accessible endpoint to retrieve contractors for user registration.
    """
    return db.query(Contractor).offset(skip).limit(limit).all()

@router.get("/companies", response_model=List[schemas.CompanyResponse])
def read_public_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Publicly accessible endpoint to retrieve companies for user registration.
    """
    return db.query(Company).offset(skip).limit(limit).all()
