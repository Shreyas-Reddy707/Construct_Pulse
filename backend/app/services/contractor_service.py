from sqlalchemy.orm import Session
from app.models.models import Contractor, User
from app.schemas import schemas

class ContractorService:
    @classmethod
    def get_contractors(cls, db: Session, current_user: User, skip: int = 0, limit: int = 100):
        query = db.query(Contractor)
        if current_user.company_id:
            query = query.filter(Contractor.company_id == current_user.company_id)
        return query.offset(skip).limit(limit).all()

    @classmethod
    def create_contractor(cls, db: Session, current_user: User, contractor_in: schemas.ContractorCreate) -> Contractor:
        contractor_data = contractor_in.model_dump()
        if current_user.company_id:
            contractor_data["company_id"] = current_user.company_id
        contractor = Contractor(**contractor_data)
        db.add(contractor)
        return contractor
