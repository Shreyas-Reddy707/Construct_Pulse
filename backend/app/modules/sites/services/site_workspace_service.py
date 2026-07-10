from sqlalchemy.orm import Session
from app.models.models import User
from app.core.exceptions import ResourceNotFoundException
from app.modules.sites.repositories.site_repo import SiteWorkspaceRepository
from app.modules.sites.schemas.site_dto import SiteDetailResponse

class SiteWorkspaceService:
    @staticmethod
    def get_site_workspace_detail(session: Session, site_id: str, current_user: User) -> SiteDetailResponse:
        # 1. Fetch from repository with tenant isolation
        site = SiteWorkspaceRepository.get_site_workspace_by_id(
            session=session,
            site_id=site_id,
            company_id=current_user.company_id
        )
        
        # 2. Trap cross-tenant or missing resources
        if not site:
            raise ResourceNotFoundException("Site not found")
            
        # 3. Build Presentation DTO
        return SiteDetailResponse(
            id=site.id,
            name=site.name,
            code=site.code,
            status=site.status,
            supervisor=site.supervisor_name,
            municipality=site.municipality,
            current_occupancy=site.current_occupancy,
            max_occupancy=site.max_occupancy,
            project_manager_name=site.project_manager.name if site.project_manager else None
        )
