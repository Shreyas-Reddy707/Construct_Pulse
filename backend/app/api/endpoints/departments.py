from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import User, UserRole
from app.api.deps import get_current_user, RoleChecker
from app.services.department_service import DepartmentService
from app.modules.departments.services.department_workspace_service import DepartmentWorkspaceService
from app.modules.departments.schemas.department_dto import DepartmentDetailResponse

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse[schemas.DepartmentResponse])
def read_departments(
    query: schemas.DepartmentQuery = Depends(), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    items, total = DepartmentService.get_departments(db, current_user, query)
    return schemas.PaginatedResponse.create(data=items, total_records=total, skip=query.skip, limit=query.limit)

@router.post("/", response_model=schemas.DepartmentResponse)
def create_department(
    department_in: schemas.DepartmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker([UserRole.COMPANY_ADMIN]))
):
    department = DepartmentService.create_department(db, current_user, department_in)
    db.refresh(department)
    return department

@router.get("/{department_id}/workspace", response_model=DepartmentDetailResponse)
def read_department_workspace(
    department_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return DepartmentWorkspaceService.get_department_workspace_detail(db, department_id, current_user)
