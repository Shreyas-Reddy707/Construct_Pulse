from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class DepartmentDetailResponse(BaseModel):
    id: str
    name: str
    department_code: Optional[str] = None
    status: Optional[str] = None
    head: Optional[str] = None
    head_name: Optional[str] = None
    head_phone: Optional[str] = None
    head_email: Optional[str] = None
    worker_count: int
    total_workers: int
    active_sites: int
    assigned_sites: List[str]
    created_at: datetime
