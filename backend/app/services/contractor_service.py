from sqlalchemy.orm import Session
from app.models.models import Contractor, User
from app.schemas import schemas

class ContractorService:
    SEARCH_FIELDS = [Contractor.name]
    SORTABLE_FIELDS = {
        "name": Contractor.name,
        "created_at": Contractor.created_at,
    }

    @classmethod
    def get_contractors(cls, db: Session, current_user: User, query):
        from app.services.query_helper import apply_search, apply_sort
        
        db_query = db.query(Contractor)
        if current_user.company_id:
            db_query = db_query.filter(Contractor.company_id == current_user.company_id)
            
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
    def create_contractor(cls, db: Session, current_user: User, contractor_in: schemas.ContractorCreate) -> Contractor:
        contractor_data = contractor_in.model_dump()
        if current_user.company_id:
            contractor_data["company_id"] = current_user.company_id
        contractor = Contractor(**contractor_data)
        db.add(contractor)
        return contractor
