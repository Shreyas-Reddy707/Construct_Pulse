from sqlalchemy.orm import Session, joinedload
from app.models.models import User, UserRole

class WorkerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_worker_by_id(self, worker_id: str, company_id: str) -> User | None:
        return self.db.query(User).options(
            joinedload(User.department),
            joinedload(User.contractor)
        ).filter(
            User.id == worker_id,
            User.company_id == company_id,
            User.role == UserRole.WORKER,
            User.is_deleted == False
        ).first()
