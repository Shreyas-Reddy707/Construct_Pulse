from pydantic import BaseModel
from typing import Optional
from app.models.models import WorkerStatus

class DepartmentReference(BaseModel):
    id: str
    name: str

class ContractorReference(BaseModel):
    id: str
    name: str

class WorkerDetailResponse(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    badge_id: Optional[str]
    status: WorkerStatus
    phone: Optional[str]
    emergency_contact: Optional[str] = None
    department: Optional[DepartmentReference] = None
    contractor: Optional[ContractorReference] = None

    class Config:
        from_attributes = True
        orm_mode = True
