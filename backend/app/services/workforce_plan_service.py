from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    WorkforcePlan, WorkforcePlanDepartment, WorkforcePlanContractor, WorkforcePlanAuditLog,
    PlanStatus, PlanSource, Site, Department, Contractor
)
from app.schemas.schemas import (
    WorkforcePlanCreate, WorkforcePlanResponse, DepartmentTargetCreate, ContractorTargetCreate,
    PlanningDashboard, PlanningSummary, DepartmentTargetResponse, ContractorTargetResponse
)

class WorkforcePlanService:
    """
    Public Service Contract:
    WorkforcePlanService is the exclusive public interface for the Workforce Planning Foundation.
    Future domains (Payroll, Reporting, Compliance) must consume WorkforcePlanService 
    and never query WorkforcePlan ORMs directly.
    """

    @classmethod
    def _generate_plan_number(cls, db: Session) -> str:
        # Architectural Documentation: Sequence generation is database-driven to ensure atomic, gapless sequence numbers under concurrent load.
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('workforce_plan_number_seq')).scalar()
        return f"WFP-{year}-{seq_val:06d}"

    @classmethod
    def _map_department_to_dto(cls, dept: WorkforcePlanDepartment) -> DepartmentTargetResponse:
        return DepartmentTargetResponse(
            id=dept.id,
            department_id=dept.department_id,
            planned_headcount=dept.planned_headcount
        )

    @classmethod
    def _map_contractor_to_dto(cls, contractor: WorkforcePlanContractor) -> ContractorTargetResponse:
        return ContractorTargetResponse(
            id=contractor.id,
            contractor_id=contractor.contractor_id,
            planned_headcount=contractor.planned_headcount
        )

    @classmethod
    def _map_plan_to_dto(cls, plan: WorkforcePlan) -> WorkforcePlanResponse:
        return WorkforcePlanResponse(
            id=plan.id,
            company_id=plan.company_id,
            site_id=plan.site_id,
            plan_number=plan.plan_number,
            target_date=plan.target_date,
            plan_status=plan.plan_status,
            plan_source=plan.plan_source,
            plan_version=plan.plan_version,
            created_by=plan.created_by,
            approved_by=plan.approved_by,
            approved_at=plan.approved_at,
            archived_at=plan.archived_at,
            created_at=plan.created_at,
            departments=[cls._map_department_to_dto(d) for d in plan.departments],
            contractors=[cls._map_contractor_to_dto(c) for c in plan.contractors]
        )

    @classmethod
    def _create_audit_log(cls, db: Session, plan_id: str, plan_version: int, plan_source: PlanSource, audit_batch_id: str, old_status: Optional[PlanStatus], new_status: Optional[PlanStatus], performed_by: str, reason: str):
        # Architectural Documentation: Audit logs are append-only to preserve a verifiable chain of custody for all state changes.
        audit = WorkforcePlanAuditLog(
            workforce_plan_id=plan_id,
            plan_version=plan_version,
            plan_source=plan_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def create_draft(cls, db: Session, company_id: str, current_user_id: str, payload: WorkforcePlanCreate) -> WorkforcePlanResponse:
        from app.core.exceptions import ResourceNotFoundException, ValidationException, StateTransitionException, ConflictException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        # Validate site
        site = db.query(Site).filter(Site.id == payload.site_id, Site.company_id == company_id).first()
        if not site:
            raise ResourceNotFoundException("Site not found")

        existing_plan = db.query(WorkforcePlan).filter(
            WorkforcePlan.company_id == company_id,
            WorkforcePlan.site_id == payload.site_id,
            WorkforcePlan.target_date == payload.target_date
        ).first()

        if existing_plan:
            raise ConflictException("A workforce plan already exists for this site on this date")

        plan_number = cls._generate_plan_number(db)

        # Lifecycle Documentation: DRAFT
        # - planning stage
        # - editable
        
        # Architectural Documentation: PlanSource exists to distinguish between manual entry, API creation, or bulk import.
        # Architectural Documentation: Planning never owns actual workforce. Actual workforce belongs to Attendance.
        plan = WorkforcePlan(
            company_id=company_id,
            site_id=payload.site_id,
            plan_number=plan_number,
            target_date=payload.target_date,
            plan_status=PlanStatus.DRAFT,
            plan_source=PlanSource.MANUAL,
            created_by=current_user_id
        )
        db.add(plan)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            plan_id=plan.id,
            plan_version=plan.plan_version,
            plan_source=plan.plan_source,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=PlanStatus.DRAFT,
            performed_by=current_user_id,
            reason="Workforce plan draft created"
        )
        db.commit()
        db.refresh(plan)
        return cls._map_plan_to_dto(plan)

    @classmethod
    def set_department_targets(cls, db: Session, company_id: str, plan_id: str, current_user_id: str, targets: List[DepartmentTargetCreate]) -> WorkforcePlanResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        plan = db.query(WorkforcePlan).filter(WorkforcePlan.id == plan_id, WorkforcePlan.company_id == company_id).first()
        if not plan:
            raise ResourceNotFoundException("Plan not found")
            
        if plan.plan_status != PlanStatus.DRAFT:
            raise StateTransitionException("Only DRAFT plans can have targets updated")

        for t in targets:
            dept = db.query(Department).filter(Department.id == t.department_id, Department.company_id == company_id).first()
            if not dept:
                raise ResourceNotFoundException(f"Department {t.department_id} not found")

        # Clear existing targets for simple replacement
        db.query(WorkforcePlanDepartment).filter(WorkforcePlanDepartment.workforce_plan_id == plan.id).delete()

        # Planning Target Documentation: Department Targets represent planned workforce expectations—not actual workforce.
        # Actual workforce always belongs to Attendance. This preserves strict domain separation.
        for t in targets:
            dept_target = WorkforcePlanDepartment(
                workforce_plan_id=plan.id,
                department_id=t.department_id,
                planned_headcount=t.planned_headcount
            )
            db.add(dept_target)

        # Architectural Documentation: Plan versions exist to guarantee precise point-in-time state correlation for audits.
        # Verify plan_version increments consistently for every state-changing operation (Prepares for optimistic locking)
        plan.plan_version += 1
        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            plan_id=plan.id,
            plan_version=plan.plan_version,
            plan_source=plan.plan_source,
            audit_batch_id=audit_batch_id,
            old_status=plan.plan_status,
            new_status=plan.plan_status,
            performed_by=current_user_id,
            reason="Department targets updated"
        )
        db.commit()
        db.refresh(plan)
        return cls._map_plan_to_dto(plan)

    @classmethod
    def set_contractor_targets(cls, db: Session, company_id: str, plan_id: str, current_user_id: str, targets: List[ContractorTargetCreate]) -> WorkforcePlanResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        plan = db.query(WorkforcePlan).filter(WorkforcePlan.id == plan_id, WorkforcePlan.company_id == company_id).first()
        if not plan:
            raise ResourceNotFoundException("Plan not found")
            
        if plan.plan_status != PlanStatus.DRAFT:
            raise StateTransitionException("Only DRAFT plans can have targets updated")

        for t in targets:
            contractor = db.query(Contractor).filter(Contractor.id == t.contractor_id, Contractor.company_id == company_id).first()
            if not contractor:
                raise ResourceNotFoundException(f"Contractor {t.contractor_id} not found")

        # Clear existing targets for simple replacement
        db.query(WorkforcePlanContractor).filter(WorkforcePlanContractor.workforce_plan_id == plan.id).delete()

        # Planning Target Documentation: Contractor Targets represent planned workforce expectations—not actual workforce.
        # Actual workforce always belongs to Attendance. This preserves strict domain separation.
        for t in targets:
            contractor_target = WorkforcePlanContractor(
                workforce_plan_id=plan.id,
                contractor_id=t.contractor_id,
                planned_headcount=t.planned_headcount
            )
            db.add(contractor_target)

        # Verify plan_version increments consistently for every state-changing operation
        plan.plan_version += 1
        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            plan_id=plan.id,
            plan_version=plan.plan_version,
            plan_source=plan.plan_source,
            audit_batch_id=audit_batch_id,
            old_status=plan.plan_status,
            new_status=plan.plan_status,
            performed_by=current_user_id,
            reason="Contractor targets updated"
        )
        db.commit()
        db.refresh(plan)
        return cls._map_plan_to_dto(plan)

    @classmethod
    def approve(cls, db: Session, company_id: str, plan_id: str, current_user_id: str, reason: str) -> WorkforcePlanResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        plan = db.query(WorkforcePlan).filter(WorkforcePlan.id == plan_id, WorkforcePlan.company_id == company_id).first()
        if not plan:
            raise ResourceNotFoundException("Plan not found")
            
        if plan.plan_status != PlanStatus.DRAFT:
            raise StateTransitionException("Only DRAFT plans can be approved")

        # Lifecycle Documentation: APPROVED
        # - operational baseline
        # - immutable
        old_status = plan.plan_status
        plan.plan_status = PlanStatus.APPROVED
        plan.approved_by = current_user_id
        plan.approved_at = datetime.now(timezone.utc)
        
        # Verify plan_version increments consistently for every state-changing operation
        plan.plan_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            plan_id=plan.id,
            plan_version=plan.plan_version,
            plan_source=plan.plan_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=plan.plan_status,
            performed_by=current_user_id,
            reason=f"Plan approved: {reason}"
        )
        db.commit()
        db.refresh(plan)
        return cls._map_plan_to_dto(plan)

    @classmethod
    def archive(cls, db: Session, company_id: str, plan_id: str, current_user_id: str, reason: str) -> WorkforcePlanResponse:
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        plan = db.query(WorkforcePlan).filter(WorkforcePlan.id == plan_id, WorkforcePlan.company_id == company_id).first()
        if not plan:
            raise ResourceNotFoundException("Plan not found")
            
        if plan.plan_status != PlanStatus.APPROVED:
            raise StateTransitionException("Only APPROVED plans can be archived")

        # Lifecycle Documentation: ARCHIVED
        # - historical record
        # - excluded from active planning
        old_status = plan.plan_status
        plan.plan_status = PlanStatus.ARCHIVED
        plan.archived_at = datetime.now(timezone.utc)
        
        # Verify plan_version increments consistently for every state-changing operation
        plan.plan_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            plan_id=plan.id,
            plan_version=plan.plan_version,
            plan_source=plan.plan_source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=plan.plan_status,
            performed_by=current_user_id,
            reason=f"Plan archived: {reason}"
        )
        db.commit()
        db.refresh(plan)
        return cls._map_plan_to_dto(plan)

    @classmethod
    def get_plan(cls, db: Session, company_id: str, plan_id: str) -> Optional[WorkforcePlanResponse]:
        plan = db.query(WorkforcePlan).filter(WorkforcePlan.id == plan_id, WorkforcePlan.company_id == company_id).first()
        if plan:
            return cls._map_plan_to_dto(plan)
        return None

    @classmethod
    def list_plans(cls, db: Session, company_id: str, site_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[WorkforcePlanResponse]:
        query = db.query(WorkforcePlan).filter(WorkforcePlan.company_id == company_id)
        if site_id:
            query = query.filter(WorkforcePlan.site_id == site_id)
        
        plans = query.order_by(WorkforcePlan.created_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_plan_to_dto(p) for p in plans]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> PlanningDashboard:
        counts = db.query(
            WorkforcePlan.plan_status, 
            func.count(WorkforcePlan.id)
        ).filter(
            WorkforcePlan.company_id == company_id
        ).group_by(WorkforcePlan.plan_status).all()

        counts_dict = {status: count for status, count in counts}

        summary = PlanningSummary(
            draft=counts_dict.get(PlanStatus.DRAFT, 0),
            approved=counts_dict.get(PlanStatus.APPROVED, 0),
            archived=counts_dict.get(PlanStatus.ARCHIVED, 0)
        )

        return PlanningDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
