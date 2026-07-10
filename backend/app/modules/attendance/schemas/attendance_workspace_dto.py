from pydantic import BaseModel
from typing import List

class AttendanceLogResponse(BaseModel):
    id: str
    attendance_id: str
    worker_id: str
    site_id: str
    site_name: str
    scan_type: str
    timestamp: str

class AttendancePageResponse(BaseModel):
    items: List[AttendanceLogResponse]
    total_records: int
    skip: int
    limit: int
