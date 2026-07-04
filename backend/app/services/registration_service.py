from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fastapi import HTTPException
from datetime import datetime
import uuid

from app.models.models import RegistrationRequest, User, SiteQRCode, RegistrationStatus, RegistrationSource
from app.schemas.schemas import RegistrationRequestCreate
from app.services.secure_token_service import SecureTokenService

class RegistrationService:

    @classmethod
    def validate_request(cls, session: Session, qr_token: str) -> SiteQRCode:
        """
        Validates the token and retrieves the associated token record.
        """
        status = SecureTokenService.validate_token(session, qr_token)
        if status != "VALID":
            raise HTTPException(status_code=400, detail=f"Invalid or {status.lower()} registration token.")

        qr_record = session.query(SiteQRCode).filter(SiteQRCode.qr_token == qr_token).first()
        if not qr_record:
            raise HTTPException(status_code=400, detail="Site could not be resolved from token.")
            
        return qr_record

    @classmethod
    def detect_duplicates(cls, session: Session, phone_number: str, email: str = None) -> None:
        """
        Detects duplicates across existing RegistrationRequests and Users.
        """
        # Check Users (Active identities)
        # Any existing User with this phone or email blocks a new registration request.
        user_query = session.query(User).filter(User.phone_number == phone_number)
        if email:
            user_query = session.query(User).filter(
                or_(User.phone_number == phone_number, User.email == email)
            )
        
        if user_query.first():
            raise HTTPException(status_code=400, detail="A user with this phone number or email already exists.")

        # Check RegistrationRequests (In-flight applications)
        # Active registrations (PENDING, UNDER_REVIEW, APPROVED) prevent duplicates.
        # Terminal registrations (REJECTED, WITHDRAWN) do not permanently block future applications.
        reg_query = session.query(RegistrationRequest).filter(
            RegistrationRequest.phone_number == phone_number,
            RegistrationRequest.status.in_([
                RegistrationStatus.PENDING, 
                RegistrationStatus.UNDER_REVIEW, 
                RegistrationStatus.APPROVED
            ])
        )
        
        if email:
            reg_query = session.query(RegistrationRequest).filter(
                or_(
                    RegistrationRequest.phone_number == phone_number,
                    RegistrationRequest.email == email
                ),
                RegistrationRequest.status.in_([
                    RegistrationStatus.PENDING, 
                    RegistrationStatus.UNDER_REVIEW, 
                    RegistrationStatus.APPROVED
                ])
            )
            
        if reg_query.first():
            raise HTTPException(status_code=400, detail="An active registration request with this phone number or email already exists.")

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
        qr_record = cls.validate_request(session, req_in.qr_token)
        
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
            requested_company_id=req_in.requested_company_id,
            requested_site_id=qr_record.site_id,
            status=RegistrationStatus.PENDING,
            payload=req_in.payload,
            payload_version=1,
            registration_source=RegistrationSource.SECURE_TOKEN,
            secure_token_generation=qr_record.generation,
            submitted_from_token=req_in.qr_token
        )
        
        session.add(req_obj)
        session.commit()
        session.refresh(req_obj)
        
        return req_obj

    @classmethod
    def get_request(cls, session: Session, request_id: str) -> RegistrationRequest:
        req = session.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()
        if not req:
            raise HTTPException(status_code=404, detail="Registration request not found.")
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
