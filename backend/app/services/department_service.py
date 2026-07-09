from sqlalchemy.orm import Session
from app.models.models import Department, User
from app.schemas import schemas

class DepartmentService:
    @classmethod
    def get_departments(cls, db: Session, current_user: User, skip: int = 0, limit: int = 100):
        query = db.query(Department)
        if current_user.company_id:
            query = query.filter(Department.company_id == current_user.company_id)
        return query.offset(skip).limit(limit).all()

    @classmethod
    def create_department(cls, db: Session, current_user: User, department_in: schemas.DepartmentCreate) -> Department:
        dept_data = department_in.model_dump()
        if current_user.company_id:
            dept_data["company_id"] = current_user.company_id
        department = Department(**dept_data)
        db.add(department)
        return department
