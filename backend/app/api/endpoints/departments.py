from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole
from app.api.deps import get_current_user, RoleChecker
from app.services.department_service import DepartmentService

router = APIRouter()

@router.get("/", response_model=List[schemas.DepartmentResponse])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return DepartmentService.get_departments(db, current_user, skip, limit)

@router.post("/", response_model=schemas.DepartmentResponse)
def create_department(
    department_in: schemas.DepartmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    department = DepartmentService.create_department(db, current_user, department_in)
    db.refresh(department)
    return department
