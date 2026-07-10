from sqlalchemy.orm import Session
from app.models.models import User
from app.core.exceptions import ResourceNotFoundException
from app.modules.contractors.repositories.contractor_repo import ContractorWorkspaceRepository
from app.modules.contractors.schemas.contractor_dto import ContractorDetailResponse

class ContractorWorkspaceService:
    @staticmethod
    def get_contractor_workspace_detail(session: Session, contractor_id: str, current_user: User) -> ContractorDetailResponse:
        # 1. Fetch from repository with tenant isolation
        result = ContractorWorkspaceRepository.get_contractor_workspace_by_id(
            session=session,
            contractor_id=contractor_id,
            company_id=current_user.company_id
        )
        
        # 2. Trap cross-tenant or missing resources
        if not result:
            raise ResourceNotFoundException("Contractor not found")
            
        contractor, total_workers, active_workers, active_sites = result
        
        # 3. Handle primary contact resolution safely
        primary_contact_name = None
        primary_contact_phone = None
        primary_contact_email = None
        
        if contractor.primary_contact:
            primary_contact_name = contractor.primary_contact.name
            primary_contact_phone = contractor.primary_contact.phone_number
            # email is not explicitly in User right now but we use what we have or leave None
            # If firebase_uid is email or something else, but for now we'll stick to schema contract
            # Let's map it safely if available. Wait, User model might not have email.
            pass
            
        compliance_status_str = None
        if contractor.compliance_status:
            compliance_status_str = contractor.compliance_status.value
            
        company_name = contractor.company.name if contractor.company else ""
            
        # 4. Build Presentation DTO
        return ContractorDetailResponse(
            id=contractor.id,
            name=contractor.name,
            company=company_name,
            status=contractor.operational_status,  # Map operational_status -> status
            assigned_sites=[],  # Hardcoded empty list per FSD profile rules
            worker_count=total_workers,  # Using total_workers for worker_count as well
            contract_expiry=contractor.contract_expiry,
            created_at=contractor.created_at,
            total_workers=total_workers,
            active_workers=active_workers,
            active_sites=active_sites,
            primary_contact_name=primary_contact_name,
            primary_contact_phone=primary_contact_phone or contractor.phone, # fallback to legacy phone
            primary_contact_email=primary_contact_email,
            operational_status=contractor.operational_status,
            compliance_status=compliance_status_str
        )
