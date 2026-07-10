from sqlalchemy.orm import Session
from app.models.models import User
from app.core.exceptions import ResourceNotFoundException
from app.modules.departments.repositories.department_repo import DepartmentWorkspaceRepository
from app.modules.departments.schemas.department_dto import DepartmentDetailResponse

class DepartmentWorkspaceService:
    @staticmethod
    def get_department_workspace_detail(session: Session, department_id: str, current_user: User) -> DepartmentDetailResponse:
        # 1. Fetch from repository with tenant isolation
        result = DepartmentWorkspaceRepository.get_department_workspace_by_id(
            session=session,
            department_id=department_id,
            company_id=current_user.company_id
        )
        
        # 2. Trap cross-tenant or missing resources
        if not result:
            raise ResourceNotFoundException("Department not found")
            
        department, total_workers, active_sites = result
        
        # 3. Handle department head resolution safely
        head_name = None
        head_phone = None
        head_email = None
        head = None
        
        if department.department_head:
            head_name = department.department_head.name
            head_phone = department.department_head.phone_number
            head = department.department_head.name # Legacy fallback
            # email is not explicitly mapped for User in standard schema right now, but we prepare the slot
            
        status_str = department.status.value if department.status else None
            
        # 4. Build Presentation DTO
        return DepartmentDetailResponse(
            id=department.id,
            name=department.name,
            department_code=department.department_code,
            status=status_str,
            head=head,
            head_name=head_name,
            head_phone=head_phone,
            head_email=head_email,
            worker_count=total_workers,
            total_workers=total_workers,
            active_sites=active_sites,
            assigned_sites=[],  # Hardcoded empty list per FSD profile rules
            created_at=department.created_at
        )
