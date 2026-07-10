from typing import Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.models import Department, User, UserRole, department_to_site

class DepartmentWorkspaceRepository:
    @staticmethod
    def get_department_workspace_by_id(session: Session, department_id: str, company_id: str) -> Optional[Tuple[Department, int, int]]:
        # Define scalar subqueries
        total_workers_sq = (
            session.query(func.count(User.id))
            .filter(
                User.department_id == department_id, 
                User.role == UserRole.WORKER, 
                User.is_deleted == False
            )
            .correlate(Department)
            .scalar_subquery()
        )
        
        active_sites_sq = (
            session.query(func.count(func.distinct(department_to_site.c.site_id)))
            .filter(department_to_site.c.department_id == department_id)
            .correlate(Department)
            .scalar_subquery()
        )
        
        # Build main query
        query = (
            session.query(
                Department,
                total_workers_sq.label("total_workers"),
                active_sites_sq.label("active_sites")
            )
            .filter(Department.id == department_id, Department.is_deleted == False)
            .filter(Department.company_id == company_id)
            .options(
                joinedload(Department.department_head)
            )
        )
        
        return query.first()
