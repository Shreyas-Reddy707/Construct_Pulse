from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ContractorDetailResponse(BaseModel):
    id: str
    name: str
    company: str
    status: Optional[str] = None
    assigned_sites: List[str]
    worker_count: int
    contract_expiry: Optional[datetime] = None
    created_at: datetime
    
    total_workers: int
    active_workers: int
    active_sites: int
    primary_contact_name: Optional[str] = None
    primary_contact_phone: Optional[str] = None
    primary_contact_email: Optional[str] = None
    operational_status: Optional[str] = None
    compliance_status: Optional[str] = None
