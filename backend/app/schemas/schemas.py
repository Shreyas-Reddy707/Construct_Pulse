from pydantic import BaseModel, Field, root_validator, validator, AnyHttpUrl
from typing import Optional, List, TypeVar, Generic
import math

try:
    from pydantic.generics import GenericModel
    PaginationBase = GenericModel
except ImportError:
    PaginationBase = BaseModel

T = TypeVar('T')

class PaginationMetadata(BaseModel):
    total_records: int
    skip: int
    limit: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class PaginatedResponse(PaginationBase, Generic[T]):
    data: List[T]
    metadata: PaginationMetadata

    @classmethod
    def create(cls, data: List[T], total_records: int, skip: int, limit: int):
        page_size = len(data)
        total_pages = math.ceil(total_records / limit) if limit > 0 else 1
        has_next = (skip + limit) < total_records
        has_previous = skip > 0
        return cls(
            data=data,
            metadata=PaginationMetadata(
                total_records=total_records,
                skip=skip,
                limit=limit,
                page_size=page_size,
                total_pages=total_pages,
                has_next=has_next,
                has_previous=has_previous
            )
        )
from datetime import datetime
from app.models.models import (
    UserRole, AttendanceStatus, WorkerStatus,
    Role, SiteStatus, PlanSource, PlanStatus,
    NotificationPriority, NotificationType,
    AdjustmentType, PayrollSource, PayrollStatus, ReportStatus, ReportSource, ReportType, AttendanceMethod, GovernanceAction, AttendanceReasonCode, SnapshotSource, MusterSessionStatus, MusterParticipantStatus, MusterParticipantType, IncidentStatus, IncidentSeverity, ParticipantRole, EvidenceType, IncidentSource, VisitorVisitStatus, VisitSource, ObservationType, ObservationStatus, CorrectiveActionStatus, RiskSeverity, ObservationSource, CorrectiveActionSource, CommunicationStatus, CommunicationSource, RecipientStatus, NotificationSource, ConfigCategory, ConfigurationStatus, ConfigurationSource, RegistrationStatus
)

class BaseQuery(BaseModel):
    search: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None
    skip: int = 0
    limit: int = 100

    @validator('limit')
    def limit_max_1000(cls, v):
        if v > 1000:
            raise ValueError("limit must not exceed 1000")
        return v

    @validator('sort_order')
    def sort_order_valid(cls, v):
        if v and v.lower() not in ['asc', 'desc']:
            raise ValueError("sort_order must be asc or desc")
        return v.lower() if v else None

class UserQuery(BaseQuery):
    status: Optional[WorkerStatus] = None
    role: Optional[UserRole] = None
    department_id: Optional[str] = None
    contractor_id: Optional[str] = None
    site_id: Optional[str] = None

class SiteQuery(BaseQuery):
    status: Optional[SiteStatus] = None

class DepartmentQuery(BaseQuery):
    pass

class ContractorQuery(BaseQuery):
    pass

class RegistrationQuery(BaseQuery):
    status: Optional[RegistrationStatus] = None

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
from datetime import datetime

class AccessRequirement(BaseModel):
    code: str
    message: str
    severity: str

class AccessDecision(BaseModel):
    allowed: bool
    reasons: List[AccessRequirement]
    evaluated_at: datetime

class ReadinessRequirement(BaseModel):
    code: str
    message: str

class WorkerReadinessResponse(BaseModel):
    ready: bool
    missing: List[ReadinessRequirement]

class SiteReadinessResponse(BaseModel):
    status: str
    ready: bool
    missing: List[ReadinessRequirement]

class SiteSuspendRequest(BaseModel):
    reason: Optional[str] = None

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
    status: Optional[str] = "draft"
    company_id: str
    working_hours: Optional[str] = None
    capacity: Optional[int] = None
    muster_point: Optional[str] = None
    primary_emergency_contact_name: Optional[str] = None
    primary_emergency_contact_phone: Optional[str] = None
    secondary_emergency_contact_name: Optional[str] = None
    secondary_emergency_contact_phone: Optional[str] = None
    suspension_reason: Optional[str] = None
    activated_by: Optional[str] = None
    activated_at: Optional[datetime] = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geofence_radius_meters: Optional[float] = None
    status: Optional[str] = None
    working_hours: Optional[str] = None
    capacity: Optional[int] = None
    muster_point: Optional[str] = None
    primary_emergency_contact_name: Optional[str] = None
    primary_emergency_contact_phone: Optional[str] = None
    secondary_emergency_contact_name: Optional[str] = None
    secondary_emergency_contact_phone: Optional[str] = None
    suspension_reason: Optional[str] = None

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
    check_in_method: AttendanceMethod
    check_out_method: Optional[AttendanceMethod] = None

    class Config:
        from_attributes = True

# --- Reporting Schemas ---
class AttendanceReportQuery(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    worker_id: Optional[str] = None
    site_id: Optional[str] = None
    company_id: Optional[str] = None
    status: Optional[str] = None
    sort_by: Optional[str] = "check_in_time"
    sort_order: Optional[str] = "desc"
    skip: int = 0
    limit: int = 100

    @validator('limit')
    def limit_max_1000(cls, v):
        if v > 1000:
            raise ValueError("limit must not exceed 1000")
        return v

    @validator('sort_order')
    def sort_order_valid(cls, v):
        if v.lower() not in ['asc', 'desc']:
            raise ValueError("sort_order must be asc or desc")
        return v.lower()

    @validator('sort_by')
    def sort_by_valid(cls, v):
        allowed = ["check_in_time", "check_out_time", "status"]
        if v not in allowed:
            raise ValueError(f"sort_by must be one of {allowed}")
        return v

    @root_validator(skip_on_failure=True)
    def check_dates(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        if start and end and start > end:
            raise ValueError('start_date must be before or equal to end_date')
        return values

class AttendanceReportRow(BaseModel):
    attendance_id: str
    worker_id: str
    worker_name: Optional[str] = None
    site_id: str
    site_name: Optional[str] = None
    company_id: Optional[str] = None
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    status: str
    check_in_method: Optional[str] = None
    check_out_method: Optional[str] = None
    correction_count: int = 0
    has_corrections: bool = False

    class Config:
        from_attributes = True

class ReportMetadata(BaseModel):
    total_records: int
    returned_records: int
    skip: int
    limit: int
    applied_filters: dict

class AttendanceReportResponse(BaseModel):
    report_id: str
    generated_at: datetime
    metadata: ReportMetadata
    rows: List[AttendanceReportRow]

# --- Governance Schemas ---
class AdminCheckoutRequest(BaseModel):
    reason_code: AttendanceReasonCode
    reason_notes: Optional[str] = None

class AttendanceCorrectionRequest(BaseModel):
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    reason_code: AttendanceReasonCode
    reason_notes: Optional[str] = None

class AttendanceCorrectionLogResponse(BaseModel):
    id: str
    attendance_id: str
    correction_batch_id: str
    attendance_version: int
    governance_action: GovernanceAction
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason_code: AttendanceReasonCode
    reason_notes: Optional[str] = None
    performed_by: str
    approved_by: Optional[str] = None
    performed_at: datetime

    class Config:
        from_attributes = True

class GovernanceResult(BaseModel):
    correction_batch_id: str
    attendance_version: int
    fields_modified: List[str]
    performed_at: datetime

# --- Occupancy Schemas ---
class OccupancyQuery(BaseModel):
    site_id: Optional[str] = None
    department_id: Optional[str] = None
    contractor_id: Optional[str] = None
    include_visitors: bool = True
    skip: int = 0
    limit: int = 100

class OccupancySummary(BaseModel):
    total_present: int
    active_workers: int
    active_visitors: int
    active_contractors: int
    site_id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class OccupancyWorker(BaseModel):
    attendance_id: str
    worker_id: str
    worker_name: str
    identity_type: str
    department_name: Optional[str] = None
    contractor_name: Optional[str] = None
    check_in_time: datetime

    class Config:
        from_attributes = True

class DepartmentOccupancy(BaseModel):
    department_id: str
    department_name: str
    worker_count: int

class ContractorOccupancy(BaseModel):
    contractor_id: str
    contractor_name: str
    worker_count: int

class VisitorOccupancy(BaseModel):
    visitor_count: int

class OccupancyDashboard(BaseModel):
    summary: OccupancySummary
    department_breakdown: List[DepartmentOccupancy]
    contractor_breakdown: List[ContractorOccupancy]
    visitor_breakdown: VisitorOccupancy
    total_occupancy: int
    capacity: Optional[int] = None
    remaining_capacity: Optional[int] = None

class OccupancySnapshotResponse(BaseModel):
    snapshot_id: str
    site_id: str
    captured_at: datetime
    snapshot_source: SnapshotSource
    captured_by: Optional[str] = None
    total_occupancy: int
    department_breakdown: dict
    contractor_breakdown: dict
    visitor_breakdown: dict = {}

    class Config:
        from_attributes = True

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

from app.models.models import RegistrationStatus, IdentityType, RegistrationSource
from typing import Dict, Any

class RegistrationRequestCreate(BaseModel):
    identity_type: IdentityType
    full_name: str
    phone_number: str
    email: Optional[str] = None
    requested_company_id: Optional[str] = None
    qr_token: str
    payload: Optional[Dict[str, Any]] = None

class RegistrationRequestResponse(BaseModel):
    id: str
    registration_number: str
    identity_type: IdentityType
    full_name: str
    phone_number: str
    email: Optional[str] = None
    requested_company_id: Optional[str] = None
    requested_site_id: str
    status: RegistrationStatus
    payload: Optional[Dict[str, Any]] = None
    payload_version: int
    registration_source: RegistrationSource
    submitted_at: datetime
    secure_token_generation: Optional[int] = None
    submitted_from_token: Optional[str] = None
    review_notes: Optional[str] = None
    approval_notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_user_id: Optional[str] = None

    class Config:
        from_attributes = True

class RegistrationReviewRequest(BaseModel):
    notes: Optional[str] = None

# --- Emergency Muster Schemas ---

class MusterSessionBase(BaseModel):
    site_id: str
    emergency_type: str
    notes: Optional[str] = None

class MusterSessionCreate(MusterSessionBase):
    pass

class MusterSessionResponse(MusterSessionBase):
    id: str
    company_id: str
    occupancy_snapshot_id: Optional[str] = None
    initiated_by: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    status: MusterSessionStatus

    class Config:
        from_attributes = True

class MusterParticipantResponse(BaseModel):
    id: str
    muster_session_id: str
    attendance_id: Optional[str] = None
    user_id: str
    participant_type: MusterParticipantType
    status: MusterParticipantStatus
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None

    class Config:
        from_attributes = True

class MusterSummary(BaseModel):
    safe_count: int
    missing_count: int
    unaccounted_count: int
    manually_accounted_count: int
    total_participants: int

class MusterDashboard(BaseModel):
    session: MusterSessionResponse
    summary: MusterSummary

class MusterOverrideRequest(BaseModel):
    status: MusterParticipantStatus
    reason: Optional[str] = None

# --- Incident Management Schemas ---
class IncidentCreate(BaseModel):
    site_id: str
    severity: IncidentSeverity = IncidentSeverity.LOW
    title: str
    description: Optional[str] = None

class IncidentResponse(BaseModel):
    id: str
    incident_number: str
    company_id: str
    site_id: str
    reported_by: str
    assigned_to: Optional[str] = None
    severity: IncidentSeverity
    status: IncidentStatus
    title: str
    description: Optional[str] = None
    reported_at: datetime
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    incident_version: int
    incident_source: IncidentSource

    class Config:
        from_attributes = True

class IncidentParticipantCreate(BaseModel):
    user_id: Optional[str] = None
    participant_name: Optional[str] = None
    role: ParticipantRole
    notes: Optional[str] = None

class IncidentParticipantResponse(BaseModel):
    id: str
    incident_id: str
    user_id: Optional[str] = None
    participant_name: Optional[str] = None
    role: ParticipantRole
    notes: Optional[str] = None
    added_at: datetime

    class Config:
        from_attributes = True

class IncidentEvidenceCreate(BaseModel):
    evidence_type: EvidenceType
    reference: str
    description: Optional[str] = None

class IncidentEvidenceResponse(BaseModel):
    id: str
    incident_id: str
    evidence_type: EvidenceType
    reference: str
    description: Optional[str] = None
    uploaded_by: str
    uploaded_at: datetime
    evidence_version: int

    class Config:
        from_attributes = True

class IncidentSummary(BaseModel):
    draft: int
    reported: int
    under_investigation: int
    resolved: int
    closed: int

class IncidentDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: IncidentSummary

class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
    reason: str

class IncidentAssign(BaseModel):
    assigned_to: str
    reason: str


class VisitorVisitCreate(BaseModel):
    visitor_id: str
    host_id: str
    site_id: str
    purpose: Optional[str] = None
    valid_from: datetime
    valid_until: datetime
    visit_source: VisitSource = VisitSource.HOST

class VisitorVisitResponse(BaseModel):
    id: str
    visit_number: str
    visitor_id: str
    host_id: str
    company_id: str
    site_id: str
    visit_status: VisitorVisitStatus
    visit_source: VisitSource
    visit_version: int
    purpose: Optional[str] = None
    valid_from: datetime
    valid_until: datetime
    checked_in_at: Optional[datetime] = None
    checked_out_at: Optional[datetime] = None
    badge_identifier: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VisitorVisitSummary(BaseModel):
    requested: int
    approved: int
    active: int
    completed: int
    cancelled: int
    expired: int

class VisitorDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: VisitorVisitSummary

class VisitorAuditResponse(BaseModel):
    id: str
    visit_id: str
    old_status: Optional[VisitorVisitStatus] = None
    new_status: Optional[VisitorVisitStatus] = None
    performed_by: str
    performed_at: datetime
    reason: str
    visit_version: int
    audit_batch_id: str

    class Config:
        from_attributes = True

# Safety Operations Foundation Schemas

class CorrectiveActionCreate(BaseModel):
    assigned_to: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class CorrectiveActionResponse(BaseModel):
    id: str
    observation_id: str
    assigned_to: str
    action_status: CorrectiveActionStatus
    action_source: CorrectiveActionSource
    corrective_action_version: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SafetyObservationCreate(BaseModel):
    site_id: str
    observation_type: ObservationType
    severity: RiskSeverity
    title: str
    description: str
    assigned_to: Optional[str] = None

class SafetyObservationResponse(BaseModel):
    id: str
    observation_number: str
    company_id: str
    site_id: str
    reported_by: str
    assigned_to: Optional[str] = None
    observation_type: ObservationType
    severity: RiskSeverity
    observation_status: ObservationStatus
    observation_source: ObservationSource
    observation_version: int
    title: str
    description: str
    created_at: datetime
    closed_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    actions: List[CorrectiveActionResponse] = []

    class Config:
        from_attributes = True

class ObservationAuditResponse(BaseModel):
    id: str
    observation_id: str
    observation_version: int
    observation_source: ObservationSource
    audit_batch_id: str
    old_status: Optional[ObservationStatus]
    new_status: Optional[ObservationStatus]
    performed_by: str
    performed_at: datetime
    reason: str

    class Config:
        from_attributes = True

class SafetySummary(BaseModel):
    reported: int
    in_progress: int
    verified: int
    closed: int
    cancelled: int

class SafetyDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: SafetySummary

class ObservationStatusUpdate(BaseModel):
    status: ObservationStatus
    reason: str

class CorrectiveActionStatusUpdate(BaseModel):
    status: CorrectiveActionStatus
    reason: str

class VisitDeny(BaseModel):
    reason: str

class VisitCancel(BaseModel):
    reason: str

class CommunicationCreate(BaseModel):
    site_id: Optional[str] = None
    title: str
    content: str
    requires_acknowledgement: bool = False

class CommunicationAcknowledgementResponse(BaseModel):
    id: str
    communication_id: str
    user_id: str
    acknowledged_at: datetime
    communication_version: int

    class Config:
        from_attributes = True

class CommunicationResponse(BaseModel):
    id: str
    company_id: str
    site_id: Optional[str]
    author_id: str
    communication_number: str
    communication_version: int
    communication_source: CommunicationSource
    status: CommunicationStatus
    title: str
    content: str
    requires_acknowledgement: bool
    created_at: datetime
    published_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    acknowledgements: List[CommunicationAcknowledgementResponse] = []

    class Config:
        from_attributes = True

class CommunicationAuditResponse(BaseModel):
    id: str
    communication_id: str
    communication_version: int
    communication_source: CommunicationSource
    audit_batch_id: str
    old_status: Optional[CommunicationStatus]
    new_status: Optional[CommunicationStatus]
    performed_by: str
    performed_at: datetime
    reason: str

    class Config:
        from_attributes = True

class CommunicationSummary(BaseModel):
    draft: int
    published: int
    archived: int
    requiring_acknowledgement: int

class CommunicationDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: CommunicationSummary

class PublishCommunicationRequest(BaseModel):
    reason: str

class ArchiveCommunicationRequest(BaseModel):
    reason: str

class AcknowledgeCommunicationRequest(BaseModel):
    reason: Optional[str] = None

class DepartmentTargetCreate(BaseModel):
    department_id: str
    planned_headcount: int

class ContractorTargetCreate(BaseModel):
    contractor_id: str
    planned_headcount: int

class WorkforcePlanCreate(BaseModel):
    site_id: str
    target_date: datetime

class DepartmentTargetResponse(BaseModel):
    id: str
    department_id: str
    planned_headcount: int

    class Config:
        from_attributes = True

class ContractorTargetResponse(BaseModel):
    id: str
    contractor_id: str
    planned_headcount: int

    class Config:
        from_attributes = True

class WorkforcePlanResponse(BaseModel):
    id: str
    company_id: str
    site_id: str
    plan_number: str
    target_date: datetime
    plan_status: PlanStatus
    plan_source: PlanSource
    plan_version: int
    created_by: str
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    created_at: datetime
    departments: List[DepartmentTargetResponse] = []
    contractors: List[ContractorTargetResponse] = []

    class Config:
        from_attributes = True

class PlanningSummary(BaseModel):
    draft: int
    approved: int
    archived: int

class PlanningDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: PlanningSummary

class ApprovePlanRequest(BaseModel):
    reason: str

class ArchivePlanRequest(BaseModel):
    reason: str

class NotificationCreate(BaseModel):
    site_id: Optional[str] = None
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority
    target_user_ids: List[str] = []
    target_role: Optional[UserRole] = None

class NotificationRecipientResponse(BaseModel):
    id: str
    user_id: str
    recipient_status: RecipientStatus
    read_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: str
    company_id: str
    site_id: Optional[str] = None
    notification_number: str
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority
    notification_source: NotificationSource
    notification_version: int
    created_by: str
    created_at: datetime
    recipients: List[NotificationRecipientResponse] = []

    class Config:
        from_attributes = True

class NotificationSummary(BaseModel):
    unread: int
    read: int
    archived: int

class NotificationDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: NotificationSummary

class NotificationReadRequest(BaseModel):
    reason: Optional[str] = None

class NotificationArchiveRequest(BaseModel):
    reason: Optional[str] = None


# --- PAYROLL FOUNDATION DTOs ---

class PayrollRunCreate(BaseModel):
    site_id: Optional[str] = None
    start_date: datetime
    end_date: datetime

class PayrollAdjustmentCreate(BaseModel):
    adjustment_type: AdjustmentType
    amount: float
    reason: str

class PayrollAdjustmentResponse(BaseModel):
    id: str
    payroll_employee_id: str
    adjustment_type: AdjustmentType
    amount: float
    reason: str

    class Config:
        from_attributes = True

class PayrollEmployeeResponse(BaseModel):
    id: str
    payroll_run_id: str
    user_id: str
    regular_hours: float
    overtime_hours: float
    total_hours: float
    base_rate: float
    total_amount: float
    worker_name: str
    employee_number: str
    department_name: str
    contractor_name: Optional[str] = None
    adjustments: List[PayrollAdjustmentResponse] = []

    class Config:
        from_attributes = True

class PayrollAuditResponse(BaseModel):
    id: str
    payroll_run_id: str
    payroll_version: int
    audit_batch_id: str
    old_status: Optional[PayrollStatus] = None
    new_status: Optional[PayrollStatus] = None
    performed_by: str
    performed_at: datetime
    reason: str

    class Config:
        from_attributes = True

class PayrollRunResponse(BaseModel):
    id: str
    company_id: str
    site_id: Optional[str] = None
    payroll_number: str
    start_date: datetime
    end_date: datetime
    payroll_status: PayrollStatus
    payroll_source: PayrollSource
    payroll_version: int
    created_by: str
    approved_by: Optional[str] = None
    created_at: datetime
    approved_at: Optional[datetime] = None
    locked_at: Optional[datetime] = None
    employees: List[PayrollEmployeeResponse] = []

    class Config:
        from_attributes = True

class PayrollSummary(BaseModel):
    draft: int
    approved: int
    locked: int

class PayrollDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: PayrollSummary

# ==========================================
# REPORTING & COMPLIANCE FOUNDATION (BATCH 6D)
# ==========================================

from typing import Any, Dict

class ReportGenerateRequest(BaseModel):
    report_type: ReportType
    site_id: Optional[str] = None
    parameters: Dict[str, Any] = {} # Arbitrary parameters for report generation, e.g., start_date, end_date

class ComplianceReportSnapshotResponse(BaseModel):
    id: str
    compliance_report_id: str
    snapshot_data: Dict[str, Any]
    
    class Config:
        from_attributes = True

class ComplianceReportResponse(BaseModel):
    id: str
    company_id: str
    site_id: Optional[str] = None
    report_number: str
    report_type: ReportType
    report_status: ReportStatus
    report_source: ReportSource
    report_version: int
    generated_by: str
    generated_at: datetime
    archived_at: Optional[datetime] = None
    snapshot: Optional[ComplianceReportSnapshotResponse] = None

    class Config:
        from_attributes = True

class ReportSummary(BaseModel):
    generated: int
    archived: int

class ReportDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: ReportSummary

class ReportAuditResponse(BaseModel):
    id: str
    compliance_report_id: str
    report_version: int
    audit_batch_id: str
    old_status: Optional[ReportStatus]
    new_status: Optional[ReportStatus]
    performed_by: str
    performed_at: datetime
    reason: str

    class Config:
        from_attributes = True


# ==========================================
# PLATFORM CONFIGURATION DTOs (BATCH 6E)
# ==========================================

class ConfigurationDraftRequest(BaseModel):
    site_id: Optional[str] = None
    config_key: str
    category: ConfigCategory
    config_value: dict

class ConfigurationApproveRequest(BaseModel):
    reason: str

class ConfigurationVersionResponse(BaseModel):
    id: str
    configuration_id: str
    version_number: int
    config_value: dict
    status: ConfigurationStatus
    created_by: str
    approved_by: Optional[str]
    created_at: datetime
    approved_at: Optional[datetime]
    archived_at: Optional[datetime]

    class Config:
        from_attributes = True

class ConfigurationResponse(BaseModel):
    id: str
    company_id: str
    site_id: Optional[str]
    configuration_number: str
    config_key: str
    category: ConfigCategory
    configuration_source: ConfigurationSource
    created_by: str
    created_at: datetime
    active_version: Optional[ConfigurationVersionResponse] = None
    
    class Config:
        from_attributes = True

class ConfigurationAuditResponse(BaseModel):
    id: str
    configuration_version_id: str
    version_number: int
    configuration_source: ConfigurationSource
    audit_batch_id: str
    old_status: Optional[ConfigurationStatus]
    new_status: Optional[ConfigurationStatus]
    performed_by: str
    performed_at: datetime
    reason: str

    class Config:
        from_attributes = True

class ConfigurationSummary(BaseModel):
    draft: int
    active: int
    archived: int

class ConfigurationDashboard(BaseModel):
    report_id: str
    generated_at: datetime
    summary: ConfigurationSummary
