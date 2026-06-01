from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class FirebaseLogin(BaseModel):
    token: str

class UserBase(BaseModel):
    phone_number: str
    name: str
    role: UserRole = UserRole.WORKER
    employee_id: Optional[str] = None

class UserCreate(UserBase):
    firebase_uid: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    company_id: Optional[str] = None
    department_id: Optional[str] = None
    contractor_id: Optional[str] = None

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: str

    class Config:
        from_attributes = True

class ContractorBase(BaseModel):
    name: str
    phone: Optional[str] = None
    trade: Optional[str] = None
    company_id: Optional[str] = None

class ContractorCreate(ContractorBase):
    pass

class ContractorResponse(ContractorBase):
    id: str

    class Config:
        from_attributes = True

# --- Site Schemas ---
class SiteBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geofence_radius_meters: Optional[float] = 100.0
    status: Optional[str] = "active"
    company_id: str

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geofence_radius_meters: Optional[float] = None
    status: Optional[str] = None

class SiteResponse(SiteBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class SiteAssignment(BaseModel):
    worker_id: Optional[str] = None
    department_id: Optional[str] = None
    contractor_id: Optional[str] = None

class SiteAssignmentsResponse(BaseModel):
    workers: List[str] = []
    departments: List[str] = []
    contractors: List[str] = []

# --- QR Management ---
class QRCodeResponse(BaseModel):
    qr_token: str
    qr_image: Optional[str] = None
    expires_at: datetime

    class Config:
        from_attributes = True

# --- Attendance Schemas ---
class AttendanceCheckIn(BaseModel):
    site_id: str
    qr_token: str
    gps_latitude: float
    gps_longitude: float

class AttendanceCheckOut(BaseModel):
    site_id: str
    qr_token: str
    gps_latitude: float
    gps_longitude: float

class AttendanceResponse(BaseModel):
    id: str
    user_id: str
    site_id: str
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    status: str

    class Config:
        from_attributes = True

# --- Occupancy Schemas ---
class OccupancyResponse(BaseModel):
    total_workers: int
    department_breakdown: dict
    contractor_breakdown: dict

    class Config:
        from_attributes = True
