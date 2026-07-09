from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime

from app.models.models import (
    RegistrationRequest, 
    RegistrationStatus, 
    User, 
    WorkerStatus, 
    Site,
    worker_to_site,
    Company
)
from app.services.identity_mapper import IdentityMapper
from app.core.exceptions import ResourceNotFoundException, StateTransitionException, ConflictException, AuthorizationException

class ApprovalService:
    SEARCH_FIELDS = [RegistrationRequest.worker_first_name, RegistrationRequest.worker_last_name, RegistrationRequest.worker_email]
    SORTABLE_FIELDS = {
        "name": RegistrationRequest.worker_last_name,
        "email": RegistrationRequest.worker_email,
        "status": RegistrationRequest.status,
        "created_at": RegistrationRequest.created_at,
    }

    @classmethod
    def fetch_pending_requests(cls, session: Session, company_id: str, query):
        """
        Fetch registration requests securely scoped to the company.
        """
        from app.services.query_helper import apply_search, apply_sort
        
        # Sites belonging to this company
        site_subquery = session.query(Site.id).filter(Site.company_id == company_id).subquery()
        
        db_query = session.query(RegistrationRequest).filter(
            or_(
                RegistrationRequest.requested_company_id == company_id,
                RegistrationRequest.requested_site_id.in_(site_subquery)
            )
        )
        
        # Filtering - FORCE queue states (Issue 2 Remediation)
        db_query = db_query.filter(RegistrationRequest.status.in_([RegistrationStatus.PENDING, RegistrationStatus.UNDER_REVIEW]))
            
        # Searching
        db_query = apply_search(db_query, query.search, cls.SEARCH_FIELDS)
        
        # Count BEFORE Sort (Issue 1 Remediation)
        total_count = db_query.count()
        
        # Sorting
        db_query = apply_sort(
            db_query, 
            query.sort_by, 
            query.sort_order, 
            cls.SORTABLE_FIELDS, 
            default_sort_field="created_at",
            default_sort_order="desc"
        )
        
        items = db_query.offset(query.skip).limit(query.limit).all()
        return items, total_count

    @classmethod
    def get_request(cls, session: Session, request_id: str, company_id: str) -> RegistrationRequest:
        """
        Retrieve a specific request securely scoped to the company.
        """
        site_subquery = session.query(Site.id).filter(Site.company_id == company_id).subquery()
        req = session.query(RegistrationRequest).filter(
            RegistrationRequest.id == request_id,
            or_(
                RegistrationRequest.requested_company_id == company_id,
                RegistrationRequest.requested_site_id.in_(site_subquery)
            )
        ).first()
        
        if not req:
            raise ResourceNotFoundException("Registration request not found or access denied")
        return req

    @classmethod
    def move_to_under_review(cls, session: Session, request_id: str, admin: User) -> RegistrationRequest:
        """
        Move a request to UNDER_REVIEW status atomically.
        """
        site_subquery = session.query(Site.id).filter(Site.company_id == admin.company_id).subquery()
        req = session.query(RegistrationRequest).filter(
            RegistrationRequest.id == request_id,
            or_(
                RegistrationRequest.requested_company_id == admin.company_id,
                RegistrationRequest.requested_site_id.in_(site_subquery)
            )
        ).with_for_update().first()
        
        if not req:
            raise ResourceNotFoundException("Registration request not found or access denied")
            
        if req.status != RegistrationStatus.PENDING:
            raise StateTransitionException("Only PENDING requests can be moved to UNDER_REVIEW")
            
        req.status = RegistrationStatus.UNDER_REVIEW
        session.commit()
        session.refresh(req)
        return req

    @classmethod
    def reject_request(cls, session: Session, request_id: str, admin: User, notes: str = None) -> RegistrationRequest:
        """
        Reject a registration request.
        """
        req = session.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).with_for_update().first()
        if not req:
            raise ResourceNotFoundException("Request not found")
            
        # Security validation
        cls.get_request(session, request_id, admin.company_id)

        if req.status not in [RegistrationStatus.PENDING, RegistrationStatus.UNDER_REVIEW]:
            raise StateTransitionException(f"Cannot reject request in {req.status.value} status")
            
        req.status = RegistrationStatus.REJECTED
        if notes:
            req.approval_notes = notes
        req.approved_by = admin.id
        req.approved_at = datetime.utcnow()
        
        session.commit()
        session.refresh(req)
        return req

    @classmethod
    def approve_request(cls, session: Session, request_id: str, admin: User, notes: str = None) -> User:
        """
        Atomically approve a registration request, create the User, and assign them.
        """
        # 1. Acquire row lock to prevent double approval concurrency
        req = session.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).with_for_update().first()
        if not req:
            raise ResourceNotFoundException("Registration request not found")

        # 2. Validate Manager Authorization
        # Site resolution
        site = session.query(Site).filter(Site.id == req.requested_site_id).first()
        if not site:
            raise ResourceNotFoundException("Requested site is invalid")
            
        req_company_id = req.requested_company_id or site.company_id
        if admin.company_id and req_company_id != admin.company_id:
            raise AuthorizationException("Unauthorized to approve for this company")

        # 3. Validate Request Status
        if req.status not in [RegistrationStatus.PENDING, RegistrationStatus.UNDER_REVIEW]:
            raise StateTransitionException(f"Request is already {req.status.value}")

        # 4. Duplicate Detection (Final safeguard before user creation)
        phone = req.phone_number
        user_query = session.query(User).filter(User.phone_number == phone)
        if user_query.first():
            raise ConflictException("A User with this phone number already exists")

        # 5. Extract Payload and Create User
        payload = req.payload or {}
        
        new_user = User(
            name=req.full_name,
            phone_number=req.phone_number,
            role=IdentityMapper.get_role(req.identity_type),
            company_id=req_company_id,
            department_id=payload.get("department_id"),
            contractor_id=payload.get("contractor_id"),
            is_active=True,
            status=WorkerStatus.APPROVED,
            designation=payload.get("designation"),
            emergency_contact_name=payload.get("emergency_contact_name"),
            emergency_contact_phone=payload.get("emergency_contact_phone"),
            employee_id=payload.get("employee_id")
        )
        
        session.add(new_user)
        session.flush() # Flush to get new_user.id
        
        # 6. Assign Site
        # By default requested_site becomes the assigned site
        # Note: raw insert for association table
        session.execute(worker_to_site.insert().values(user_id=new_user.id, site_id=site.id))
        
        # 7. Update RegistrationRequest
        req.status = RegistrationStatus.APPROVED
        req.created_user_id = new_user.id
        req.approved_by = admin.id
        req.approved_at = datetime.utcnow()
        if notes:
            req.approval_notes = notes
            
        # 8. Commit Transaction (Handled automatically by FastAPI Depends, but we do it explicitly to be safe)
        session.commit()
        session.refresh(new_user)
        
        return new_user
