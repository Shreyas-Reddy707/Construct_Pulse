from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Department, User, UserRole
from app.api.deps import get_current_user, RoleChecker

router = APIRouter()

@router.get("", response_model=List[schemas.DepartmentResponse])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Department)
    if current_user.company_id:
        query = query.filter(Department.company_id == current_user.company_id)
    departments = query.offset(skip).limit(limit).all()
    return departments

@router.post("/", response_model=schemas.DepartmentResponse)
def create_department(
    department_in: schemas.DepartmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    dept_data = department_in.model_dump()
    if current_user.company_id:
        dept_data["company_id"] = current_user.company_id
    department = Department(**dept_data)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department
