from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, Enum, Table, JSON, Index, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid
import enum

class ContractorComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REVIEW_PENDING = "review_pending"

class DepartmentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class WorkerStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

class SiteStatus(str, enum.Enum):
    DRAFT = "draft"
    CONFIGURED = "configured"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"

class RegistrationStatus(str, enum.Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class IdentityType(str, enum.Enum):
    WORKER = "WORKER"
    VISITOR = "VISITOR"
    CONTRACTOR_REPRESENTATIVE = "CONTRACTOR_REPRESENTATIVE"
    SITE_ENGINEER = "SITE_ENGINEER"
    INSPECTOR = "INSPECTOR"
    VENDOR = "VENDOR"

class RegistrationSource(str, enum.Enum):
    SECURE_TOKEN = "SECURE_TOKEN"
    ADMIN = "ADMIN"
    API = "API"
    IMPORT = "IMPORT"
    SELF_SERVICE = "SELF_SERVICE"

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

class SnapshotSource(str, enum.Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"
    EVENT = "EVENT"

class MusterSessionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class MusterParticipantStatus(str, enum.Enum):
    UNACCOUNTED = "UNACCOUNTED"
    SAFE = "SAFE"
    MISSING = "MISSING"
    MANUALLY_ACCOUNTED = "MANUALLY_ACCOUNTED"

class MusterParticipantType(str, enum.Enum):
    WORKER = "WORKER"
    VISITOR = "VISITOR"
    CONTRACTOR = "CONTRACTOR"
    ENGINEER = "ENGINEER"
    INSPECTOR = "INSPECTOR"

class IncidentStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    REPORTED = "REPORTED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    WITHDRAWN = "WITHDRAWN"

class IncidentSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IncidentSource(str, enum.Enum):
    MANUAL = "MANUAL"
    MUSTER = "MUSTER"
    API = "API"
    IMPORT = "IMPORT"

class ParticipantRole(str, enum.Enum):
    REPORTER = "REPORTER"
    INJURED = "INJURED"
    WITNESS = "WITNESS"
    INVOLVED = "INVOLVED"
    RESPONDER = "RESPONDER"

class EvidenceType(str, enum.Enum):
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    TEXT = "TEXT"

class VisitorVisitStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class ObservationType(str, enum.Enum):
    HAZARD = "HAZARD"
    SAFE_ACT = "SAFE_ACT"
    NEAR_MISS = "NEAR_MISS"

class ObservationStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class CorrectiveActionStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class CorrectiveActionSource(str, enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    SYSTEM = "SYSTEM"

class RiskSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ObservationSource(str, enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"

class CommunicationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class CommunicationSource(str, enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"

class VisitSource(str, enum.Enum):
    HOST = "HOST"
    SELF_SERVICE = "SELF_SERVICE"
    IMPORT = "IMPORT"
    ADMIN = "ADMIN"

class UserRole(str, enum.Enum):
    WORKER = "Worker"
    SUPERVISOR = "Supervisor"
    CONTRACTOR = "Contractor"
    COMPANY_ADMIN = "Company Admin"
    MUNICIPALITY_OFFICER = "Municipality Officer"
    SYSTEM_ADMIN = "System Admin"
    COMPANY_DIRECTOR = "Company Director"
    OPERATIONS_MANAGER = "Operations Manager"
    PROJECT_MANAGER = "Project Manager"
    SITE_MANAGER = "Site Manager"
    SAFETY_OFFICER = "Safety Officer"
    VISITOR = "Visitor"

class AttendanceStatus(str, enum.Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    ABSENT = "absent"
    LEAVE = "leave"

class AttendanceMethod(str, enum.Enum):
    SECURE_TOKEN = "SECURE_TOKEN"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE"
    SYSTEM = "SYSTEM"

class GovernanceAction(str, enum.Enum):
    ADMIN_CHECKOUT = "ADMIN_CHECKOUT"
    TIME_CORRECTION = "TIME_CORRECTION"
    VOID_ATTENDANCE = "VOID_ATTENDANCE"

class AttendanceReasonCode(str, enum.Enum):
    FORGOT_CHECKOUT = "FORGOT_CHECKOUT"
    TIME_CORRECTION = "TIME_CORRECTION"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE"

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

worker_to_site = Table(
    'worker_to_site', Base.metadata,
    Column('worker_id', String, ForeignKey('users.id')),
    Column('site_id', String, ForeignKey('sites.id'))
)

department_to_site = Table(
    'department_to_site', Base.metadata,
    Column('department_id', String, ForeignKey('departments.id')),
    Column('site_id', String, ForeignKey('sites.id'))
)

contractor_to_site = Table(
    'contractor_to_site', Base.metadata,
    Column('contractor_id', String, ForeignKey('contractors.id')),
    Column('site_id', String, ForeignKey('sites.id'))
)

role_permission_group = Table(
    'role_permission_group', Base.metadata,
    Column('role_id', String, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('permission_group_id', String, ForeignKey('permission_groups.id', ondelete="CASCADE"), primary_key=True)
)

permission_group_permission = Table(
    'permission_group_permission', Base.metadata,
    Column('permission_group_id', String, ForeignKey('permission_groups.id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', String, ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    permission_groups = relationship("PermissionGroup", secondary=role_permission_group, back_populates="roles")

class PermissionGroup(Base):
    __tablename__ = "permission_groups"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    roles = relationship("Role", secondary=role_permission_group, back_populates="permission_groups")
    permissions = relationship("Permission", secondary=permission_group_permission, back_populates="groups")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    groups = relationship("PermissionGroup", secondary=permission_group_permission, back_populates="permissions")


class Company(SoftDeleteMixin, Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint('company_name', name='uq_company_name'),)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_name = Column(String, index=True, nullable=False)
    registration_number = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    departments = relationship("Department", back_populates="company")
    contractors = relationship("Contractor", back_populates="company")
    users = relationship("User", back_populates="company")
    sites = relationship("Site", back_populates="company")

class Department(SoftDeleteMixin, Base):
    __tablename__ = "departments"
    __table_args__ = (UniqueConstraint('company_id', 'department_code', name='uq_company_department_code'),)
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    department_code = Column(String, index=True, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(DepartmentStatus), nullable=True)
    department_head_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    company = relationship("Company", back_populates="departments")
    users = relationship("User", back_populates="department", foreign_keys="[User.department_id]")
    sites = relationship("Site", secondary=department_to_site, back_populates="assigned_departments")
    department_head = relationship("User", foreign_keys=[department_head_id])

class Contractor(SoftDeleteMixin, Base):
    __tablename__ = "contractors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    trade = Column(String)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    operational_status = Column(String, nullable=True)
    compliance_status = Column(Enum(ContractorComplianceStatus), nullable=True)
    contract_expiry = Column(DateTime(timezone=True), nullable=True)
    primary_contact_id = Column(String, ForeignKey("users.id"), nullable=True)

    company = relationship("Company", back_populates="contractors")
    users = relationship("User", back_populates="contractor", foreign_keys="[User.contractor_id]")
    sites = relationship("Site", secondary=contractor_to_site, back_populates="assigned_contractors")
    primary_contact = relationship("User", foreign_keys=[primary_contact_id])

class User(SoftDeleteMixin, Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.WORKER)
    employee_id = Column(String)
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    department_id = Column(String, ForeignKey("departments.id"), nullable=True)
    contractor_id = Column(String, ForeignKey("contractors.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(Enum(WorkerStatus), default=WorkerStatus.PENDING)
    designation = Column(String, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)


    company = relationship("Company", back_populates="users")
    department = relationship("Department", back_populates="users")
    contractor = relationship("Contractor", back_populates="users")
    attendances = relationship("Attendance", back_populates="user")
    assigned_sites = relationship("Site", secondary=worker_to_site, back_populates="assigned_workers")

    @property
    def company_name(self) -> str | None:
        return self.company.company_name if self.company else None

    @property
    def department_name(self) -> str | None:
        return self.department.name if self.department else None

    @property
    def contractor_name(self) -> str | None:
        return self.contractor.name if self.contractor else None

    @property
    def assigned_site_names(self) -> str:
        return ", ".join([s.name for s in self.assigned_sites]) if self.assigned_sites else ""

class Session(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    device_id = Column(String)
    device_name = Column(String)
    device_platform = Column(String)
    app_version = Column(String)
    login_time = Column(DateTime(timezone=True), default=func.now())
    last_activity = Column(DateTime(timezone=True), default=func.now())
    ip_address = Column(String)
    push_token = Column(String)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True))

    user = relationship("User")

class Site(SoftDeleteMixin, Base):
    __tablename__ = "sites"
    __table_args__ = (UniqueConstraint('company_id', 'name', name='uq_company_site_name'),)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    geofence_radius_meters = Column(Float, default=100.0)
    status = Column(String, default="active")
    municipality = Column(String, nullable=True)
    current_occupancy = Column(Integer, default=0, nullable=False)
    max_occupancy = Column(Integer, default=0, nullable=False)
    supervisor_name = Column(String, nullable=True)
    project_manager_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="sites")
    project_manager = relationship("User", foreign_keys=[project_manager_id])
    attendances = relationship("Attendance", back_populates="site")
    qr_codes = relationship("SiteQRCode", back_populates="site")
    assigned_workers = relationship("User", secondary=worker_to_site, back_populates="assigned_sites")
    assigned_departments = relationship("Department", secondary=department_to_site, back_populates="sites")
    assigned_contractors = relationship("Contractor", secondary=contractor_to_site, back_populates="sites")

class SiteQRCode(Base):
    __tablename__ = "site_qr_codes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id = Column(String, ForeignKey("sites.id"))
    qr_token = Column(String, unique=True, index=True)
    qr_image = Column(String)  # e.g., base64 string or URL
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    site = relationship("Site", back_populates="qr_codes")

class Attendance(Base):
    __tablename__ = "attendances"
    __table_args__ = (
        Index('ix_attendances_site_id_check_in_time', 'site_id', 'check_in_time'),
        Index('ix_attendances_user_id_check_in_time', 'user_id', 'check_in_time'),
    )
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    site_id = Column(String, ForeignKey("sites.id"))
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    check_in_time = Column(DateTime(timezone=True), server_default=func.now())
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.CHECKED_IN)
    check_in_method = Column(Enum(AttendanceMethod), default=AttendanceMethod.SECURE_TOKEN)
    check_out_method = Column(Enum(AttendanceMethod), nullable=True)
    
    # Access Metadata Snapshot
    access_token_id = Column(String, nullable=True)
    access_generation = Column(Integer, nullable=True)
    access_verified_at = Column(DateTime(timezone=True), nullable=True)

    # Governance & Optimistic Concurrency
    attendance_version = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="attendances")
    site = relationship("Site", back_populates="attendances")

    @property
    def site_name(self) -> str | None:
        return self.site.name if self.site else None

class AttendanceCorrectionLog(Base):
    __tablename__ = "attendance_correction_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    attendance_id = Column(String, ForeignKey("attendances.id"), nullable=False, index=True)
    correction_batch_id = Column(String, nullable=False, index=True)
    attendance_version = Column(Integer, nullable=False)
    governance_action = Column(Enum(GovernanceAction), nullable=False)
    field_name = Column(String, nullable=False)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    reason_code = Column(Enum(AttendanceReasonCode), nullable=False)
    reason_notes = Column(String, nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())

    attendance = relationship("Attendance")
    performer = relationship("User", foreign_keys=[performed_by])
    approver = relationship("User", foreign_keys=[approved_by])

class OccupancySnapshot(Base):
    __tablename__ = "occupancy_snapshots"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id = Column(String, ForeignKey("sites.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    total_workers = Column(Integer, default=0)
    department_breakdown = Column(JSON, default=dict)
    contractor_breakdown = Column(JSON, default=dict)
    visitor_breakdown = Column(JSON, default=dict)
    snapshot_source = Column(Enum(SnapshotSource), default=SnapshotSource.MANUAL, nullable=False)
    captured_by = Column(String, ForeignKey("users.id"), nullable=True)
    snapshot_version = Column(Integer, default=1, nullable=False)

    site = relationship("Site")
    capturer = relationship("User")
    
class InductionPackage(SoftDeleteMixin, Base):
    __tablename__ = "induction_packages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    title = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    expiry_days = Column(Integer, default=365, nullable=False)
    quiz_enabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    site = relationship("Site", backref="induction_packages")

class MusterSession(Base):
    __tablename__ = "muster_sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    site_id = Column(String, ForeignKey("sites.id"))
    occupancy_snapshot_id = Column(String, ForeignKey("occupancy_snapshots.id"), nullable=True)
    initiated_by = Column(String, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True), default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    emergency_type = Column(String)
    notes = Column(String, nullable=True)
    status = Column(Enum(MusterSessionStatus), default=MusterSessionStatus.DRAFT, nullable=False)

    site = relationship("Site")
    company = relationship("Company")
    initiator = relationship("User")
    occupancy_snapshot = relationship("OccupancySnapshot")
    participants = relationship("MusterParticipant", back_populates="session")

class MusterParticipant(Base):
    __tablename__ = "muster_participants"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    muster_session_id = Column(String, ForeignKey("muster_sessions.id"))
    attendance_id = Column(String, ForeignKey("attendances.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    participant_type = Column(Enum(MusterParticipantType), nullable=False)
    status = Column(Enum(MusterParticipantStatus), default=MusterParticipantStatus.UNACCOUNTED, nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(String, ForeignKey("users.id"), nullable=True)

    session = relationship("MusterSession", back_populates="participants")
    user = relationship("User", foreign_keys=[user_id])
    acknowledger = relationship("User", foreign_keys=[acknowledged_by])
    attendance = relationship("Attendance")

class MusterAuditLog(Base):
    __tablename__ = "muster_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_id = Column(String, ForeignKey("muster_participants.id"))
    old_status = Column(Enum(MusterParticipantStatus), nullable=True)
    new_status = Column(Enum(MusterParticipantStatus), nullable=False)
    performed_by = Column(String, ForeignKey("users.id"))
    performed_at = Column(DateTime(timezone=True), default=func.now())
    reason = Column(String, nullable=True)

    participant = relationship("MusterParticipant")
    actor = relationship("User")

class WorkerInductionRecord(Base):
    __tablename__ = "worker_induction_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_id = Column(String, ForeignKey("users.id"), nullable=False)
    package_id = Column(String, ForeignKey("induction_packages.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    worker_acknowledgement = Column(Boolean, default=False, nullable=False)
    package_version_completed = Column(Integer, nullable=False)
    
    worker = relationship("User", backref="induction_records")
    package = relationship("InductionPackage")

class QualificationType(SoftDeleteMixin, Base):
    __tablename__ = "qualification_types"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)

class QualificationRequirement(Base):
    __tablename__ = "qualification_requirements"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    designation = Column(String, nullable=False, index=True)
    qualification_type_id = Column(String, ForeignKey("qualification_types.id"), nullable=False)

    qualification_type = relationship("QualificationType")

class WorkerQualification(SoftDeleteMixin, Base):
    __tablename__ = "worker_qualifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    qualification_type_id = Column(String, ForeignKey("qualification_types.id"), nullable=False)
    certificate_number = Column(String)
    issuing_authority = Column(String)
    issue_date = Column(DateTime(timezone=True))
    expiry_date = Column(DateTime(timezone=True), nullable=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    document_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    worker = relationship("User", backref="qualifications")
    qualification_type = relationship("QualificationType")

class RegistrationRequest(Base):
    __tablename__ = "registration_requests"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    registration_number = Column(String, unique=True, index=True, nullable=False)
    identity_type = Column(Enum(IdentityType), nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=True)
    requested_company_id = Column(String, ForeignKey("companies.id"), nullable=True)
    requested_site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.PENDING, index=True)
    payload = Column(JSON, nullable=True)
    payload_version = Column(Integer, default=1, nullable=False)
    registration_source = Column(Enum(RegistrationSource), default=RegistrationSource.SECURE_TOKEN, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    secure_token_generation = Column(Integer, nullable=True)
    submitted_from_token = Column(String, nullable=True)
    review_notes = Column(String, nullable=True)
    approval_notes = Column(String, nullable=True)
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    requested_site = relationship("Site", foreign_keys=[requested_site_id])
    requested_company = relationship("Company", foreign_keys=[requested_company_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    created_user = relationship("User", foreign_keys=[created_user_id])

incident_number_seq = Sequence('incident_number_seq')

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_number = Column(String, unique=True, index=True, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    reported_by = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    severity = Column(Enum(IncidentSeverity), default=IncidentSeverity.LOW, nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.DRAFT, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    incident_version = Column(Integer, default=1, nullable=False)
    incident_source = Column(Enum(IncidentSource), default=IncidentSource.MANUAL, nullable=False)

    company = relationship("Company")
    site = relationship("Site")
    reporter = relationship("User", foreign_keys=[reported_by])
    investigator = relationship("User", foreign_keys=[assigned_to])
    participants = relationship("IncidentParticipant", back_populates="incident", cascade="all, delete-orphan")
    evidence = relationship("IncidentEvidence", back_populates="incident", cascade="all, delete-orphan")
    audit_logs = relationship("IncidentAuditLog", back_populates="incident", cascade="all, delete-orphan")

class IncidentParticipant(Base):
    __tablename__ = "incident_participants"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Nullable for external/unidentified
    participant_name = Column(String, nullable=True)  # Used if user_id is null
    role = Column(Enum(ParticipantRole), nullable=False)
    notes = Column(String, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    incident = relationship("Incident", back_populates="participants")
    user = relationship("User")

class IncidentEvidence(Base):
    __tablename__ = "incident_evidence"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    evidence_type = Column(Enum(EvidenceType), nullable=False)
    reference = Column(String, nullable=False)  # URL or ID to where the evidence is stored
    description = Column(String, nullable=True)
    uploaded_by = Column(String, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    evidence_version = Column(Integer, default=1, nullable=False)

    incident = relationship("Incident", back_populates="evidence")
    uploader = relationship("User")

class IncidentAuditLog(Base):
    __tablename__ = "incident_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    old_status = Column(Enum(IncidentStatus), nullable=True)
    new_status = Column(Enum(IncidentStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    incident = relationship("Incident", back_populates="audit_logs")
    performer = relationship("User")

visitor_visit_number_seq = Sequence('visitor_visit_number_seq')

class VisitorVisit(Base):
    __tablename__ = "visitor_visits"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_number = Column(String, unique=True, index=True, nullable=False)
    visitor_id = Column(String, ForeignKey("users.id"), nullable=False)
    host_id = Column(String, ForeignKey("users.id"), nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    visit_status = Column(Enum(VisitorVisitStatus), default=VisitorVisitStatus.REQUESTED, nullable=False)
    visit_source = Column(Enum(VisitSource), default=VisitSource.HOST, nullable=False)
    visit_version = Column(Integer, default=1, nullable=False)
    purpose = Column(String, nullable=True)
    valid_from = Column(DateTime(timezone=True), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    checked_in_at = Column(DateTime(timezone=True), nullable=True)
    checked_out_at = Column(DateTime(timezone=True), nullable=True)
    badge_identifier = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    visitor = relationship("User", foreign_keys=[visitor_id])
    host = relationship("User", foreign_keys=[host_id])
    company = relationship("Company")
    site = relationship("Site")
    audit_logs = relationship("VisitorVisitAuditLog", back_populates="visit", cascade="all, delete-orphan")

class VisitorVisitAuditLog(Base):
    __tablename__ = "visitor_visit_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String, ForeignKey("visitor_visits.id"), nullable=False)
    old_status = Column(Enum(VisitorVisitStatus), nullable=True)
    new_status = Column(Enum(VisitorVisitStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)
    visit_version = Column(Integer, nullable=False)
    audit_batch_id = Column(String, nullable=False)

    visit = relationship("VisitorVisit", back_populates="audit_logs")
    performer = relationship("User")

class SafetyObservation(Base):
    __tablename__ = "safety_observations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    observation_number = Column(String, unique=True, index=True, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    reported_by = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    observation_type = Column(Enum(ObservationType), nullable=False)
    severity = Column(Enum(RiskSeverity), nullable=False)
    observation_status = Column(Enum(ObservationStatus), default=ObservationStatus.REPORTED, nullable=False)
    observation_source = Column(Enum(ObservationSource), default=ObservationSource.MANUAL, nullable=False)
    observation_version = Column(Integer, default=1, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(String, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company")
    site = relationship("Site")
    reporter = relationship("User", foreign_keys=[reported_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
    verifier = relationship("User", foreign_keys=[verified_by])
    actions = relationship("CorrectiveAction", back_populates="observation", cascade="all, delete-orphan")
    audit_logs = relationship("SafetyObservationAuditLog", back_populates="observation", cascade="all, delete-orphan")

class CorrectiveAction(Base):
    __tablename__ = "safety_corrective_actions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    observation_id = Column(String, ForeignKey("safety_observations.id"), nullable=False)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=False)
    action_status = Column(Enum(CorrectiveActionStatus), default=CorrectiveActionStatus.OPEN, nullable=False)
    action_source = Column(Enum(CorrectiveActionSource), default=CorrectiveActionSource.MANUAL, nullable=False)
    corrective_action_version = Column(Integer, default=1, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    observation = relationship("SafetyObservation", back_populates="actions")
    assignee = relationship("User")

class SafetyObservationAuditLog(Base):
    __tablename__ = "safety_observation_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    observation_id = Column(String, ForeignKey("safety_observations.id"), nullable=False)
    observation_version = Column(Integer, nullable=False)
    observation_source = Column(Enum(ObservationSource), nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(ObservationStatus), nullable=True)
    new_status = Column(Enum(ObservationStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    observation = relationship("SafetyObservation", back_populates="audit_logs")
    performer = relationship("User")

communication_number_seq = Sequence('communication_number_seq')

class SafetyCommunication(Base):
    __tablename__ = "safety_communications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=True)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    communication_number = Column(String, unique=True, index=True, nullable=False)
    communication_version = Column(Integer, default=1, nullable=False)
    communication_source = Column(Enum(CommunicationSource), default=CommunicationSource.MANUAL, nullable=False)
    status = Column(Enum(CommunicationStatus), default=CommunicationStatus.DRAFT, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    requires_acknowledgement = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company")
    site = relationship("Site")
    author = relationship("User")
    acknowledgements = relationship("CommunicationAcknowledgement", back_populates="communication", cascade="all, delete-orphan")
    audit_logs = relationship("CommunicationAuditLog", back_populates="communication", cascade="all, delete-orphan")

class CommunicationAcknowledgement(Base):
    __tablename__ = "communication_acknowledgements"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    communication_id = Column(String, ForeignKey("safety_communications.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), server_default=func.now())
    communication_version = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('communication_id', 'user_id', name='uq_communication_user_acknowledgement'),
    )

    communication = relationship("SafetyCommunication", back_populates="acknowledgements")
    user = relationship("User")

class CommunicationAuditLog(Base):
    __tablename__ = "communication_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    communication_id = Column(String, ForeignKey("safety_communications.id"), nullable=False)
    communication_version = Column(Integer, nullable=False)
    communication_source = Column(Enum(CommunicationSource), nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(CommunicationStatus), nullable=True)
    new_status = Column(Enum(CommunicationStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    communication = relationship("SafetyCommunication", back_populates="audit_logs")
    performer = relationship("User")

class PlanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    ARCHIVED = "ARCHIVED"

class PlanSource(str, enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"

class WorkforcePlan(Base):
    __tablename__ = "workforce_plans"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    plan_number = Column(String, nullable=False, unique=True)
    target_date = Column(DateTime(timezone=True), nullable=False)
    plan_status = Column(Enum(PlanStatus), nullable=False, default=PlanStatus.DRAFT)
    plan_source = Column(Enum(PlanSource), nullable=False, default=PlanSource.MANUAL)
    plan_version = Column(Integer, nullable=False, default=1)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('company_id', 'site_id', 'target_date', name='uq_workforce_plan_site_date'),
    )

    company = relationship("Company")
    site = relationship("Site")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    departments = relationship("WorkforcePlanDepartment", back_populates="workforce_plan", cascade="all, delete-orphan")
    contractors = relationship("WorkforcePlanContractor", back_populates="workforce_plan", cascade="all, delete-orphan")
    audit_logs = relationship("WorkforcePlanAuditLog", back_populates="workforce_plan", cascade="all, delete-orphan")

class WorkforcePlanDepartment(Base):
    __tablename__ = "workforce_plan_departments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workforce_plan_id = Column(String, ForeignKey("workforce_plans.id"), nullable=False)
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    planned_headcount = Column(Integer, nullable=False)

    workforce_plan = relationship("WorkforcePlan", back_populates="departments")
    department = relationship("Department")

class WorkforcePlanContractor(Base):
    __tablename__ = "workforce_plan_contractors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workforce_plan_id = Column(String, ForeignKey("workforce_plans.id"), nullable=False)
    contractor_id = Column(String, ForeignKey("contractors.id"), nullable=False)
    planned_headcount = Column(Integer, nullable=False)

    workforce_plan = relationship("WorkforcePlan", back_populates="contractors")
    contractor = relationship("Contractor")

class WorkforcePlanAuditLog(Base):
    __tablename__ = "workforce_plan_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workforce_plan_id = Column(String, ForeignKey("workforce_plans.id"), nullable=False)
    plan_version = Column(Integer, nullable=False)
    plan_source = Column(Enum(PlanSource), nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(PlanStatus), nullable=True)
    new_status = Column(Enum(PlanStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    workforce_plan = relationship("WorkforcePlan", back_populates="audit_logs")
    performer = relationship("User")

class NotificationType(str, enum.Enum):
    SYSTEM = "SYSTEM"
    ALERT = "ALERT"
    MESSAGE = "MESSAGE"

class NotificationPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class RecipientStatus(str, enum.Enum):
    UNREAD = "UNREAD"
    READ = "READ"
    ARCHIVED = "ARCHIVED"

class NotificationSource(str, enum.Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"
    API = "API"

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=True)
    notification_number = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    priority = Column(Enum(NotificationPriority), nullable=False)
    notification_source = Column(Enum(NotificationSource), nullable=False)
    notification_version = Column(Integer, nullable=False, default=1)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company")
    site = relationship("Site")
    creator = relationship("User")
    recipients = relationship("NotificationRecipient", back_populates="notification")
    audit_logs = relationship("NotificationAuditLog", back_populates="notification")

class NotificationRecipient(Base):
    __tablename__ = "notification_recipients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id = Column(String, ForeignKey("notifications.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    recipient_status = Column(Enum(RecipientStatus), nullable=False, default=RecipientStatus.UNREAD)
    read_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)

    notification = relationship("Notification", back_populates="recipients")
    user = relationship("User")

    __table_args__ = (
        Index("ix_notification_recipients_user_status", "user_id", "recipient_status"),
        UniqueConstraint("notification_id", "user_id", name="uq_notification_user")
    )

class NotificationAuditLog(Base):
    __tablename__ = "notification_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id = Column(String, ForeignKey("notifications.id"), nullable=False)
    notification_version = Column(Integer, nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(RecipientStatus), nullable=True)
    new_status = Column(Enum(RecipientStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    notification = relationship("Notification", back_populates="audit_logs")
    performer = relationship("User")

class PayrollStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    APPROVED = "APPROVED"
    LOCKED = "LOCKED"

class AdjustmentType(str, enum.Enum):
    BONUS = "BONUS"
    DEDUCTION = "DEDUCTION"

class PayrollSource(str, enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    SYSTEM = "SYSTEM"

class PayrollRun(Base):
    __tablename__ = "payroll_runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=True)
    payroll_number = Column(String, nullable=False, unique=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    payroll_status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.DRAFT)
    payroll_source = Column(Enum(PayrollSource), nullable=False, default=PayrollSource.SYSTEM)
    payroll_version = Column(Integer, nullable=False, default=1)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    locked_at = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company")
    site = relationship("Site")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    employees = relationship("PayrollEmployee", back_populates="payroll_run")
    audit_logs = relationship("PayrollAuditLog", back_populates="payroll_run")

class PayrollEmployee(Base):
    __tablename__ = "payroll_employees"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payroll_run_id = Column(String, ForeignKey("payroll_runs.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Hours
    regular_hours = Column(Float, nullable=False, default=0.0)
    overtime_hours = Column(Float, nullable=False, default=0.0)
    total_hours = Column(Float, nullable=False, default=0.0)
    
    # Financial
    base_rate = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    
    # Historical snapshot fields
    worker_name = Column(String, nullable=False)
    employee_number = Column(String, nullable=False)
    department_name = Column(String, nullable=False)
    contractor_name = Column(String, nullable=True)

    payroll_run = relationship("PayrollRun", back_populates="employees")
    user = relationship("User")
    adjustments = relationship("PayrollAdjustment", back_populates="payroll_employee")

class PayrollAdjustment(Base):
    __tablename__ = "payroll_adjustments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payroll_employee_id = Column(String, ForeignKey("payroll_employees.id"), nullable=False)
    adjustment_type = Column(Enum(AdjustmentType), nullable=False)
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=False)

    payroll_employee = relationship("PayrollEmployee", back_populates="adjustments")

class PayrollAuditLog(Base):
    __tablename__ = "payroll_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payroll_run_id = Column(String, ForeignKey("payroll_runs.id"), nullable=False)
    payroll_version = Column(Integer, nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(PayrollStatus), nullable=True)
    new_status = Column(Enum(PayrollStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    payroll_run = relationship("PayrollRun", back_populates="audit_logs")
    performer = relationship("User")


# ==========================================
# REPORTING & COMPLIANCE FOUNDATION (BATCH 6D)
# ==========================================

import enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Sequence

class ReportStatus(enum.Enum):
    GENERATED = "GENERATED"
    ARCHIVED = "ARCHIVED"

class ReportSource(enum.Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"

class ReportType(enum.Enum):
    ATTENDANCE_COMPLIANCE = "ATTENDANCE_COMPLIANCE"
    PAYROLL_SUMMARY = "PAYROLL_SUMMARY"
    SAFETY_SUMMARY = "SAFETY_SUMMARY"
    INCIDENT_SUMMARY = "INCIDENT_SUMMARY"
    OCCUPANCY_SUMMARY = "OCCUPANCY_SUMMARY"

# PostgreSQL Sequence for Reporting
compliance_report_number_seq = Sequence('compliance_report_number_seq')

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=True)
    report_number = Column(String, unique=True, nullable=False, index=True)
    report_type = Column(Enum(ReportType), nullable=False)
    report_status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.GENERATED)
    report_source = Column(Enum(ReportSource), nullable=False, default=ReportSource.SYSTEM)
    report_version = Column(Integer, nullable=False, default=1)
    
    generated_by = Column(String, ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    archived_at = Column(DateTime(timezone=True), nullable=True)

    snapshot = relationship("ComplianceReportSnapshot", back_populates="compliance_report", uselist=False, cascade="all, delete-orphan")
    audit_logs = relationship("ReportAuditLog", back_populates="compliance_report", cascade="all, delete-orphan")
    company = relationship("Company")
    site = relationship("Site")
    generator = relationship("User")

class ComplianceReportSnapshot(Base):
    __tablename__ = "compliance_report_snapshots"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    compliance_report_id = Column(String, ForeignKey("compliance_reports.id"), nullable=False, unique=True)
    snapshot_data = Column(JSONB, nullable=False)  # Contains the immutable report output

    compliance_report = relationship("ComplianceReport", back_populates="snapshot")

class ReportAuditLog(Base):
    __tablename__ = "report_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    compliance_report_id = Column(String, ForeignKey("compliance_reports.id"), nullable=False)
    report_version = Column(Integer, nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(ReportStatus), nullable=True)
    new_status = Column(Enum(ReportStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    compliance_report = relationship("ComplianceReport", back_populates="audit_logs")
    performer = relationship("User")


# ==========================================
# PLATFORM CONFIGURATION FOUNDATION (BATCH 6E)
# ==========================================

class ConfigCategory(enum.Enum):
    GENERAL = "GENERAL"
    ATTENDANCE = "ATTENDANCE"
    PAYROLL = "PAYROLL"
    SAFETY = "SAFETY"
    NOTIFICATION = "NOTIFICATION"
    MUSTER = "MUSTER"
    OCCUPANCY = "OCCUPANCY"

class ConfigurationStatus(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class ConfigurationSource(enum.Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    API = "API"

configuration_number_seq = Sequence('configuration_number_seq')

class PlatformConfiguration(Base):
    __tablename__ = "platform_configurations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=True)
    configuration_number = Column(String, unique=True, nullable=False, index=True)
    config_key = Column(String, nullable=False, index=True)
    category = Column(Enum(ConfigCategory), nullable=False)
    configuration_source = Column(Enum(ConfigurationSource), nullable=False, default=ConfigurationSource.MANUAL)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    versions = relationship("ConfigurationVersion", back_populates="configuration", cascade="all, delete-orphan")
    company = relationship("Company")
    site = relationship("Site")
    creator = relationship("User")

class ConfigurationVersion(Base):
    __tablename__ = "configuration_versions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    configuration_id = Column(String, ForeignKey("platform_configurations.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    config_value = Column(JSONB, nullable=False)
    status = Column(Enum(ConfigurationStatus), nullable=False, default=ConfigurationStatus.DRAFT)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)

    configuration = relationship("PlatformConfiguration", back_populates="versions")
    audit_logs = relationship("ConfigurationAuditLog", back_populates="version", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])

class ConfigurationAuditLog(Base):
    __tablename__ = "configuration_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    configuration_version_id = Column(String, ForeignKey("configuration_versions.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    configuration_source = Column(Enum(ConfigurationSource), nullable=False)
    audit_batch_id = Column(String, nullable=False)
    old_status = Column(Enum(ConfigurationStatus), nullable=True)
    new_status = Column(Enum(ConfigurationStatus), nullable=True)
    performed_by = Column(String, ForeignKey("users.id"), nullable=False)
    performed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String, nullable=False)

    version = relationship("ConfigurationVersion", back_populates="audit_logs")
    performer = relationship("User")
