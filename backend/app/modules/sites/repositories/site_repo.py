from typing import Optional
from sqlalchemy.orm import Session, joinedload
from app.models.models import Site

class SiteWorkspaceRepository:
    @staticmethod
    def get_site_workspace_by_id(session: Session, site_id: str, company_id: Optional[str] = None) -> Optional[Site]:
        query = session.query(Site).filter(Site.id == site_id, Site.is_deleted == False)
        
        if company_id:
            query = query.filter(Site.company_id == company_id)
            
        # We need the project manager name, so we eagerly load the relationship
        # to avoid N+1 issues when the service maps to the DTO.
        query = query.options(joinedload(Site.project_manager))
        
        return query.first()
