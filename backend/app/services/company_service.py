from sqlalchemy.orm import Session
from app.models.models import Company, User, UserRole, Department, WorkerStatus
from app.schemas import schemas
from app.core.exceptions import ValidationException, ConflictException, ResourceNotFoundException
import logging

logger = logging.getLogger(__name__)

class CompanyService:
    @classmethod
    def create_company(cls, db: Session, company_in: schemas.CompanyCreate) -> Company:
        if not company_in.contact_phone:
            raise ValidationException("contact_phone is required to provision the initial Company Administrator")

        if company_in.registration_number:
            existing = db.query(Company).filter(Company.registration_number == company_in.registration_number).first()
            if existing:
                raise ConflictException("Registration number already exists")
                
        # 1. Create Company
        company = Company(**company_in.model_dump())
        db.add(company)
        db.flush()
        
        # 2. Create Company Administrator
        existing_user = db.query(User).filter(User.phone_number == company_in.contact_phone).first()
        if existing_user:
            raise ConflictException("Admin phone number already registered")
            
        admin_name = company_in.contact_email if company_in.contact_email else "Company Admin"
        admin_user = User(
            name=admin_name,
            phone_number=company_in.contact_phone,
            role=UserRole.COMPANY_ADMIN,
            company_id=company.id,
            is_active=False,
            status=WorkerStatus.PENDING,
            firebase_uid=f"pending_admin_{company.id}"
        )
        db.add(admin_user)
        
        # 3. Create Default Department
        default_dept = Department(
            company_id=company.id,
            name="Head Office",
            description="Default administrative department"
        )
        db.add(default_dept)
        
        return company

    @classmethod
    def assign_company_admin(cls, db: Session, company_id: str, user_id: str, current_user: User) -> User:
        target_user = db.query(User).filter(User.id == user_id, User.company_id == company_id).first()
        if not target_user:
            raise ResourceNotFoundException("User not found in this company")
            
        if target_user.role == UserRole.SYSTEM_ADMIN:
            raise ValidationException("Cannot assign SYSTEM_ADMIN as COMPANY_ADMIN")
            
        target_user.role = UserRole.COMPANY_ADMIN
        target_user.status = WorkerStatus.APPROVED
        target_user.is_active = True
        
        logger.info(f"SYSTEM_ADMIN {current_user.id} assigned COMPANY_ADMIN {target_user.id} to company {company_id}")
        
        return target_user
