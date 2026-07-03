from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole, WorkerStatus

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
    status: WorkerStatus
    company_id: Optional[str] = None
    department_id: Optional[str] = None
    contractor_id: Optional[str] = None
    company_name: Optional[str] = None
    department_name: Optional[str] = None
    contractor_name: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    assigned_site_names: Optional[str] = None

    class Config:
        from_attributes = True

class ReadinessRequirement(BaseModel):
    code: str
    message: str

class WorkerReadinessResponse(BaseModel):
    ready: bool
    missing: List[ReadinessRequirement]

class CompanyBase(BaseModel):
    company_name: str
    registration_number: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

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
    workers: List[UserResponse] = []
    departments: List[DepartmentResponse] = []
    contractors: List[ContractorResponse] = []

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
    user_name: Optional[str] = None
    company_name: Optional[str] = None
    department_name: Optional[str] = None
    contractor_name: Optional[str] = None
    site_id: str
    site_name: Optional[str] = None
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

class SiteOccupancyResponse(BaseModel):
    site_id: str
    site_name: str
    workers_on_site: int

# --- Qualification Schemas ---
class QualificationTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: Optional[str] = None

class QualificationTypeCreate(QualificationTypeBase):
    pass

class QualificationTypeResponse(QualificationTypeBase):
    id: str

    class Config:
        from_attributes = True

class WorkerQualificationBase(BaseModel):
    qualification_type_id: str
    certificate_number: Optional[str] = None
    issuing_authority: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: datetime
    document_url: Optional[str] = None

class WorkerQualificationCreate(WorkerQualificationBase):
    pass

class WorkerQualificationUpdate(BaseModel):
    verification_status: str

class WorkerQualificationResponse(WorkerQualificationBase):
    id: str
    worker_id: str
    verification_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    qualification_type: Optional[QualificationTypeResponse] = None

    class Config:
        from_attributes = True

class CompliancePassportResponse(BaseModel):
    worker_id: str
    ready: bool
    missing_requirements: List[ReadinessRequirement]
    qualifications: List[WorkerQualificationResponse]

