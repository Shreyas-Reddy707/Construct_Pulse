from typing import Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.models import Contractor, User, contractor_to_site

class ContractorWorkspaceRepository:
    @staticmethod
    def get_contractor_workspace_by_id(session: Session, contractor_id: str, company_id: str) -> Optional[Tuple[Contractor, int, int, int]]:
        # Define scalar subqueries
        total_workers_sq = (
            session.query(func.count(User.id))
            .filter(User.contractor_id == contractor_id, User.is_deleted == False)
            .correlate(Contractor)
            .scalar_subquery()
        )
        
        active_workers_sq = (
            session.query(func.count(User.id))
            .filter(User.contractor_id == contractor_id, User.is_active == True, User.is_deleted == False)
            .correlate(Contractor)
            .scalar_subquery()
        )
        
        active_sites_sq = (
            session.query(func.count(func.distinct(contractor_to_site.c.site_id)))
            .filter(contractor_to_site.c.contractor_id == contractor_id)
            .correlate(Contractor)
            .scalar_subquery()
        )
        
        # Build main query
        query = (
            session.query(
                Contractor,
                total_workers_sq.label("total_workers"),
                active_workers_sq.label("active_workers"),
                active_sites_sq.label("active_sites")
            )
            .filter(Contractor.id == contractor_id, Contractor.is_deleted == False)
            .filter(Contractor.company_id == company_id)
            .options(
                joinedload(Contractor.company),
                joinedload(Contractor.primary_contact)
            )
        )
        
        return query.first()
