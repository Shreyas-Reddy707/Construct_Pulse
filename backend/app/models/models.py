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

class UserRole(str, enum.Enum):
    WORKER = "Worker"
    SUPERVISOR = "Supervisor"
    CONTRACTOR = "Contractor"
    COMPANY_ADMIN = "Company Admin"
    MUNICIPALITY_OFFICER = "Municipality Officer"
    SYSTEM_ADMIN = "System Admin"

class AttendanceStatus(str, enum.Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    ABSENT = "absent"
    LEAVE = "leave"

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

class Company(Base):
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

class Department(Base):
    __tablename__ = "departments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    description = Column(String)

    company = relationship("Company", back_populates="departments")
    users = relationship("User", back_populates="department")
    sites = relationship("Site", secondary=department_to_site, back_populates="assigned_departments")

class Contractor(Base):
    __tablename__ = "contractors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    trade = Column(String)

    company = relationship("Company", back_populates="contractors")
    users = relationship("User", back_populates="contractor")
    sites = relationship("Site", secondary=contractor_to_site, back_populates="assigned_contractors")

class User(Base):
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

class Site(Base):
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
