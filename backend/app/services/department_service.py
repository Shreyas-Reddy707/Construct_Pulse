from sqlalchemy.orm import Session
from app.models.models import Department, User
from app.schemas import schemas

class DepartmentService:
    SEARCH_FIELDS = [Department.name]
    SORTABLE_FIELDS = {
        "name": Department.name,
        "created_at": Department.created_at,
    }

    @classmethod
    def get_departments(cls, db: Session, current_user: User, query):
        from app.services.query_helper import apply_search, apply_sort
        
        db_query = db.query(Department)
        if current_user.company_id:
            db_query = db_query.filter(Department.company_id == current_user.company_id)
            
        db_query = apply_search(db_query, query.search, cls.SEARCH_FIELDS)
        
        # Count BEFORE Sort
        total_count = db_query.count()
        
        db_query = apply_sort(
            db_query, 
            query.sort_by, 
            query.sort_order, 
            cls.SORTABLE_FIELDS, 
            default_sort_field="name",
            default_sort_order="asc"
        )
            
        items = db_query.offset(query.skip).limit(query.limit).all()
        return items, total_count

    @classmethod
    def create_department(cls, db: Session, current_user: User, department_in: schemas.DepartmentCreate) -> Department:
        dept_data = department_in.model_dump()
        if current_user.company_id:
            dept_data["company_id"] = current_user.company_id
        department = Department(**dept_data)
        db.add(department)
        return department
