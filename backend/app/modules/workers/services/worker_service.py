from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import User
from ..schemas.worker_dto import WorkerDetailResponse, DepartmentReference, ContractorReference
from ..repositories.worker_repo import WorkerRepository

class WorkerService:
    def __init__(self, db: Session):
        self.repo = WorkerRepository(db)

    def get_worker_detail(self, worker_id: str, company_id: str) -> WorkerDetailResponse:
        worker = self.repo.get_worker_by_id(worker_id, company_id)
        
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
            
        # Format emergency contact string
        emergency_contact_str = None
        if worker.emergency_contact_name or worker.emergency_contact_phone:
            parts = []
            if worker.emergency_contact_name:
                parts.append(worker.emergency_contact_name)
            if worker.emergency_contact_phone:
                parts.append(worker.emergency_contact_phone)
            emergency_contact_str = " - ".join(parts)
            if worker.emergency_contact_relationship:
                emergency_contact_str += f" ({worker.emergency_contact_relationship})"

        # Construct References
        dept_ref = None
        if worker.department:
            dept_ref = DepartmentReference(id=worker.department.id, name=worker.department.name)

        cont_ref = None
        if worker.contractor:
            cont_ref = ContractorReference(id=worker.contractor.id, name=worker.contractor.name)

        first_name = ""
        last_name = ""
        if worker.name:
            parts = worker.name.split(" ", 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        return WorkerDetailResponse(
            id=worker.id,
            first_name=first_name,
            last_name=last_name,
            badge_id=worker.employee_id,
            status=worker.status,
            phone=worker.phone_number,
            emergency_contact=emergency_contact_str,
            department=dept_ref,
            contractor=cont_ref
        )
