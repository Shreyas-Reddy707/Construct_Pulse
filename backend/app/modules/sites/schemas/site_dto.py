from typing import Optional
from pydantic import BaseModel

class ProjectManagerReference(BaseModel):
    id: str
    name: str

class SiteDetailResponse(BaseModel):
    id: str
    name: str
    code: Optional[str] = None
    status: str
    supervisor: Optional[str] = None
    municipality: Optional[str] = None
    current_occupancy: int
    max_occupancy: int
    project_manager_name: Optional[str] = None
    # We could optionally include the nested reference if the frontend is updated,
    # but the current frontend contract expects project_manager_name: string.
    # project_manager: Optional[ProjectManagerReference] = None
