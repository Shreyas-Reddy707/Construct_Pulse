from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
import uuid

from app.models.models import RegistrationRequest, User, SiteQRCode, RegistrationStatus, RegistrationSource, Site
from app.schemas.schemas import RegistrationRequestCreate
from app.services.secure_token_service import SecureTokenService

class RegistrationService:

    @classmethod
    def validate_token(cls, db: Session, token: str) -> Site:
        from app.core.exceptions import ValidationException, ResourceNotFoundException
        site = db.query(Site).filter(Site.registration_token == token).first()
        if not site:
            raise ValidationException("Invalid or inactive registration token.")
            
        if not site.is_active:
            raise ValidationException("Invalid or inactive registration token.")
            
        if not site.company_id:
            raise ResourceNotFoundException("Site could not be resolved from token.")
            
        return site

    @classmethod
    def detect_duplicates(cls, db: Session, phone_number: str, email: str = None) -> None:
        """
        Detects duplicates across existing RegistrationRequests and Users.
        """
        from app.core.exceptions import ConflictException
        # Check Users (Active identities)
        # Any existing User with this phone or email blocks a new registration request.
        existing_user = db.query(User).filter(
            or_(User.phone_number == phone_number, User.email == email)
        ).first()
        if existing_user:
            raise ConflictException("A user with this phone number or email already exists.")

        # Check RegistrationRequests (In-flight applications)
        # Active registrations (PENDING, UNDER_REVIEW, APPROVED) prevent duplicates.
        # Terminal registrations (REJECTED, WITHDRAWN) do not permanently block future applications.
        existing_req = db.query(RegistrationRequest).filter(
            or_(
                RegistrationRequest.phone_number == phone_number,
                RegistrationRequest.email == email
            ),
            RegistrationRequest.status.in_([RegistrationStatus.PENDING, RegistrationStatus.UNDER_REVIEW])
        ).first()
        if existing_req:
            raise ConflictException("An active registration request with this phone number or email already exists.")

    @classmethod
    def _generate_registration_number(cls, session: Session) -> str:
        """
        Generates a unique registration number atomically, e.g., REG-2026-000012.
        Uses a database-native sequence to ensure concurrency safety.
        """
        from sqlalchemy import Sequence
        
        current_year = datetime.now().year
        
        # Execute the sequence to get the next atomic value
        next_val = session.execute(Sequence('registration_seq'))
        
        return f"REG-{current_year}-{next_val:06d}"

    @classmethod
    def create_request(cls, session: Session, req_in: RegistrationRequestCreate) -> RegistrationRequest:
        """
        Processes a new registration request.
        """
        # 1. Validate Token
        site = cls.validate_token(session, req_in.qr_token)
        
        # 2. Detect Duplicates
        cls.detect_duplicates(session, req_in.phone_number, req_in.email)
        
        # 3. Generate Registration Number
        reg_number = cls._generate_registration_number(session)
        
        # 4. Create RegistrationRequest
        req_obj = RegistrationRequest(
            registration_number=reg_number,
            identity_type=req_in.identity_type,
            full_name=req_in.full_name,
            phone_number=req_in.phone_number,
            email=req_in.email,
            requested_company_id=site.company_id,
            requested_site_id=site.id,
            status=RegistrationStatus.PENDING,
            payload=req_in.payload,
            payload_version=1,
            registration_source=RegistrationSource.SECURE_TOKEN,
            submitted_from_token=req_in.qr_token
        )
        
        session.add(req_obj)
        session.commit()
        session.refresh(req_obj)
        
        return req_obj

    @classmethod
    def get_status(cls, db: Session, request_id: str) -> RegistrationRequest:
        from app.core.exceptions import ResourceNotFoundException
        req = db.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()
        if not req:
            raise ResourceNotFoundException("Registration request not found.")
        return req

    @classmethod
    def list_requests(cls, session: Session, site_id: str = None, company_id: str = None, status: str = None):
        query = session.query(RegistrationRequest)
        
        if site_id:
            query = query.filter(RegistrationRequest.requested_site_id == site_id)
        if company_id:
            query = query.filter(RegistrationRequest.requested_company_id == company_id)
        if status:
            query = query.filter(RegistrationRequest.status == status)
            
        return query.order_by(RegistrationRequest.submitted_at.desc()).all()
