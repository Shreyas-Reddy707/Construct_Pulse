from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Boolean, Enum, Table, JSON, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid
import enum

class WorkerStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

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
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    description = Column(String)

    company = relationship("Company", back_populates="departments")
    users = relationship("User", back_populates="department")
    sites = relationship("Site", secondary=department_to_site, back_populates="assigned_departments")

class Contractor(SoftDeleteMixin, Base):
    __tablename__ = "contractors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    trade = Column(String)

    company = relationship("Company", back_populates="contractors")
    users = relationship("User", back_populates="contractor")
    sites = relationship("Site", secondary=contractor_to_site, back_populates="assigned_contractors")

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

class Site(SoftDeleteMixin, Base):
    __tablename__ = "sites"
    __table_args__ = (UniqueConstraint('company_id', 'name', name='uq_company_site_name'),)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    geofence_radius_meters = Column(Float, default=100.0)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="sites")
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

    user = relationship("User", back_populates="attendances")
    site = relationship("Site", back_populates="attendances")

    @property
    def site_name(self) -> str | None:
        return self.site.name if self.site else None

class OccupancySnapshot(Base):
    __tablename__ = "occupancy_snapshots"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id = Column(String, ForeignKey("sites.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    total_workers = Column(Integer, default=0)
    department_breakdown = Column(JSON, default=dict)
    contractor_breakdown = Column(JSON, default=dict)

    site = relationship("Site")
    
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
