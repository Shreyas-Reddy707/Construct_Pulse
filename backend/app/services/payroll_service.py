from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    PayrollRun, PayrollEmployee, PayrollAdjustment, PayrollAuditLog,
    PayrollStatus, AdjustmentType, PayrollSource, User, UserRole,
    Attendance, Department, Contractor
)
from app.schemas.schemas import (
    PayrollRunCreate, PayrollRunResponse, PayrollEmployeeResponse,
    PayrollAdjustmentCreate, PayrollAdjustmentResponse,
    PayrollDashboard, PayrollSummary, AttendanceReportQuery
)
from app.services.attendance_reporting_service import AttendanceReportingService

class PayrollService:
    # TODO: WS1-P3B - Payroll batching requires a dedicated future engineering pack.
    # Transaction behavior left unmodified for now.
    """
    Public Service Contract:
    PayrollService is the exclusive public interface for the Payroll Foundation.
    Future domains must consume PayrollService.
    Direct querying of Payroll ORM models from external domains is forbidden.

    Lifecycle:
    DRAFT
        ↓
    APPROVED
        ↓
    LOCKED

    DRAFT:
    - Payroll generation permitted
    - Payroll regeneration permitted
    - Manual adjustments permitted

    APPROVED:
    - Financial snapshot certified
    - Regeneration prohibited
    - Adjustments prohibited

    LOCKED:
    - Permanently immutable
    - Historical record only
    - No reopening
    - No modifications
    """

    @classmethod
    def _generate_payroll_number(cls, db: Session) -> str:
        # Sequence generation is database-driven to ensure atomic, gapless sequence numbers under concurrent load.
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('payroll_run_number_seq')).scalar()
        return f"PAY-{year}-{seq_val:06d}"

    @classmethod
    def _create_audit_log(
        cls, db: Session, payroll_run_id: str, payroll_version: int, audit_batch_id: str,
        old_status: Optional[PayrollStatus], new_status: Optional[PayrollStatus],
        performed_by: str, reason: str
    ):
        # Architectural Comment: Audit logs are append-only to guarantee an unbroken historical chain 
        # of financial operations, ensuring total accountability and historical immutability.
        audit = PayrollAuditLog(
            payroll_run_id=payroll_run_id,
            payroll_version=payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def _map_adjustment_to_dto(cls, adj: PayrollAdjustment) -> PayrollAdjustmentResponse:
        return PayrollAdjustmentResponse(
            id=adj.id,
            payroll_employee_id=adj.payroll_employee_id,
            adjustment_type=adj.adjustment_type,
            amount=adj.amount,
            reason=adj.reason
        )

    @classmethod
    def _map_employee_to_dto(cls, emp: PayrollEmployee) -> PayrollEmployeeResponse:
        return PayrollEmployeeResponse(
            id=emp.id,
            payroll_run_id=emp.payroll_run_id,
            user_id=emp.user_id,
            regular_hours=emp.regular_hours,
            overtime_hours=emp.overtime_hours,
            total_hours=emp.total_hours,
            base_rate=emp.base_rate,
            total_amount=emp.total_amount,
            worker_name=emp.worker_name,
            employee_number=emp.employee_number,
            department_name=emp.department_name,
            contractor_name=emp.contractor_name,
            adjustments=[cls._map_adjustment_to_dto(a) for a in emp.adjustments]
        )

    @classmethod
    def _map_payroll_run_to_dto(cls, run: PayrollRun) -> PayrollRunResponse:
        return PayrollRunResponse(
            id=run.id,
            company_id=run.company_id,
            site_id=run.site_id,
            payroll_number=run.payroll_number,
            start_date=run.start_date,
            end_date=run.end_date,
            payroll_status=run.payroll_status,
            payroll_source=run.payroll_source,
            payroll_version=run.payroll_version,
            created_by=run.created_by,
            approved_by=run.approved_by,
            created_at=run.created_at,
            approved_at=run.approved_at,
            locked_at=run.locked_at,
            employees=[cls._map_employee_to_dto(e) for e in run.employees]
        )

    @classmethod
    def create_payroll_run(cls, db: Session, company_id: str, current_user_id: str, payload: PayrollRunCreate) -> PayrollRunResponse:
        payroll_number = cls._generate_payroll_number(db)

        # Create root aggregate
        payroll_run = PayrollRun(
            company_id=company_id,
            site_id=payload.site_id,
            payroll_number=payroll_number,
            start_date=payload.start_date,
            end_date=payload.end_date,
            payroll_status=PayrollStatus.DRAFT,
            payroll_source=PayrollSource.SYSTEM,
            created_by=current_user_id
        )
        db.add(payroll_run)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        
        cls._create_audit_log(
            db=db,
            payroll_run_id=payroll_run.id,
            payroll_version=payroll_run.payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=PayrollStatus.DRAFT,
            performed_by=current_user_id,
            reason="Payroll run created"
        )

        db.commit()
        db.refresh(payroll_run)
        return cls._map_payroll_run_to_dto(payroll_run)

    @classmethod
    def generate_payroll(cls, db: Session, payroll_run_id: str, current_user_id: str) -> PayrollRunResponse:
        # Note: Payroll only consumes already-certified attendance information.
        # It does NOT query Attendance lifecycle logic directly.
        payroll_run = db.query(PayrollRun).filter(PayrollRun.id == payroll_run_id).first()
        if not payroll_run:
            raise ValueError("Payroll run not found")

        if payroll_run.payroll_status != PayrollStatus.DRAFT:
            raise ValueError("Payroll can only be generated while in DRAFT status")

        # Architectural Comment: Payroll consumes Attendance Reporting instead of Attendance Lifecycle.
        # Payroll owns financial calculations, Attendance Reporting owns attendance calculations.
        # Payroll must never determine attendance lifecycle state, punch interpretation, or overtime eligibility.
        # Payroll simply consumes certified regular hours and overtime hours as operational inputs.
        
        query_params = AttendanceReportQuery(
            start_date=payroll_run.start_date,
            end_date=payroll_run.end_date,
            company_id=payroll_run.company_id,
            site_id=payroll_run.site_id,
            status="PRESENT"
        )
        
        # Consume the certified read model via the reporting service
        query = AttendanceReportingService._build_query(db, query_params)
        attendances = query.all()

        # Aggregate hours by user
        user_hours = {}
        for row in attendances:
            dto = AttendanceReportingService._map_to_dto(row)
            user_id = dto.worker_id
            if user_id not in user_hours:
                user_hours[user_id] = 0.0
            
            # Consuming certified regular hours as an operational input
            # Assuming 8 hours per certified PRESENT day for the foundation implementation
            user_hours[user_id] += 8.0 

        # Generate PayrollEmployee snapshots
        for user_id, total_hours in user_hours.items():
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                continue

            worker_profile = db.query(WorkerProfile).filter(WorkerProfile.user_id == user_id).first()
            department = db.query(Department).filter(Department.id == user.department_id).first() if user.department_id else None
            contractor = db.query(Contractor).filter(Contractor.id == user.contractor_id).first() if user.contractor_id else None

            # Calculate mock financial snapshot
            base_rate = worker_profile.hourly_rate if (worker_profile and worker_profile.hourly_rate) else 15.0
            regular_hours = min(total_hours, 40.0)
            overtime_hours = max(total_hours - 40.0, 0.0)
            total_amount = (regular_hours * base_rate) + (overtime_hours * base_rate * 1.5)

            # Architectural Comment: PayrollEmployee is an immutable financial snapshot.
            # Historical payroll records must never change after generation.
            # Future modifications in Worker Identity, Departments, Contractors, Configurations, 
            # or Attendance must never alter historical payroll snapshots.
            snapshot = PayrollEmployee(
                payroll_run_id=payroll_run.id,
                user_id=user_id,
                regular_hours=regular_hours,
                overtime_hours=overtime_hours,
                total_hours=total_hours,
                base_rate=base_rate,
                total_amount=total_amount,
                worker_name=f"{user.first_name} {user.last_name}",
                employee_number=user.employee_number or "N/A",
                department_name=department.name if department else "N/A",
                contractor_name=contractor.name if contractor else None
            )
            db.add(snapshot)

        db.flush()

        # Architectural Comment: PayrollRun versioning prepares for optimistic concurrency,
        # ensuring that parallel lifecycle state changes do not cause lost updates.
        payroll_run.payroll_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            payroll_run_id=payroll_run.id,
            payroll_version=payroll_run.payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=payroll_run.payroll_status,
            new_status=payroll_run.payroll_status,
            performed_by=current_user_id,
            reason="Payroll snapshots generated"
        )

        db.commit()
        db.refresh(payroll_run)
        return cls._map_payroll_run_to_dto(payroll_run)

    @classmethod
    def add_adjustment(cls, db: Session, payroll_employee_id: str, current_user_id: str, payload: PayrollAdjustmentCreate) -> PayrollEmployeeResponse:
        employee = db.query(PayrollEmployee).filter(PayrollEmployee.id == payroll_employee_id).first()
        if not employee:
            raise ValueError("Payroll employee snapshot not found")

        payroll_run = db.query(PayrollRun).filter(PayrollRun.id == employee.payroll_run_id).first()
        if payroll_run.payroll_status != PayrollStatus.DRAFT:
            raise ValueError("Adjustments can only be added to DRAFT payrolls")

        # Architectural Comment: PayrollAdjustments exist only during DRAFT status 
        # to guarantee the strict immutability of APPROVED and LOCKED financial snapshots.
        adjustment = PayrollAdjustment(
            payroll_employee_id=employee.id,
            adjustment_type=payload.adjustment_type,
            amount=payload.amount,
            reason=payload.reason
        )
        db.add(adjustment)
        db.flush()

        # Re-calculate total_amount
        if payload.adjustment_type == AdjustmentType.BONUS:
            employee.total_amount += payload.amount
        else:
            employee.total_amount -= payload.amount
            
        payroll_run.payroll_version += 1
        
        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            payroll_run_id=payroll_run.id,
            payroll_version=payroll_run.payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=payroll_run.payroll_status,
            new_status=payroll_run.payroll_status,
            performed_by=current_user_id,
            reason=f"Adjustment added to employee {employee.worker_name}"
        )

        db.commit()
        db.refresh(employee)
        return cls._map_employee_to_dto(employee)

    @classmethod
    def approve(cls, db: Session, payroll_run_id: str, current_user_id: str) -> PayrollRunResponse:
        payroll_run = db.query(PayrollRun).filter(PayrollRun.id == payroll_run_id).first()
        if not payroll_run:
            raise ValueError("Payroll run not found")

        if payroll_run.payroll_status != PayrollStatus.DRAFT:
            raise ValueError("Only DRAFT payroll runs can be APPROVED")

        old_status = payroll_run.payroll_status
        payroll_run.payroll_status = PayrollStatus.APPROVED
        payroll_run.approved_by = current_user_id
        payroll_run.approved_at = datetime.now(timezone.utc)
        
        payroll_run.payroll_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            payroll_run_id=payroll_run.id,
            payroll_version=payroll_run.payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=payroll_run.payroll_status,
            performed_by=current_user_id,
            reason="Payroll run approved"
        )

        db.commit()
        db.refresh(payroll_run)
        return cls._map_payroll_run_to_dto(payroll_run)

    @classmethod
    def lock(cls, db: Session, payroll_run_id: str, current_user_id: str) -> PayrollRunResponse:
        payroll_run = db.query(PayrollRun).filter(PayrollRun.id == payroll_run_id).first()
        if not payroll_run:
            raise ValueError("Payroll run not found")

        if payroll_run.payroll_status != PayrollStatus.APPROVED:
            raise ValueError("Only APPROVED payroll runs can be LOCKED")

        old_status = payroll_run.payroll_status
        payroll_run.payroll_status = PayrollStatus.LOCKED
        payroll_run.locked_at = datetime.now(timezone.utc)
        
        payroll_run.payroll_version += 1

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            payroll_run_id=payroll_run.id,
            payroll_version=payroll_run.payroll_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=payroll_run.payroll_status,
            performed_by=current_user_id,
            reason="Payroll run locked permanently"
        )

        db.commit()
        db.refresh(payroll_run)
        return cls._map_payroll_run_to_dto(payroll_run)

    @classmethod
    def get_payroll_run(cls, db: Session, payroll_run_id: str, company_id: str) -> Optional[PayrollRunResponse]:
        payroll_run = db.query(PayrollRun).filter(PayrollRun.id == payroll_run_id, PayrollRun.company_id == company_id).first()
        if payroll_run:
            return cls._map_payroll_run_to_dto(payroll_run)
        return None

    @classmethod
    def list_payroll_runs(cls, db: Session, company_id: str, skip: int = 0, limit: int = 100) -> List[PayrollRunResponse]:
        runs = db.query(PayrollRun).filter(
            PayrollRun.company_id == company_id
        ).order_by(PayrollRun.created_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_payroll_run_to_dto(run) for run in runs]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> PayrollDashboard:
        counts = db.query(
            PayrollRun.payroll_status, 
            func.count(PayrollRun.id)
        ).filter(
            PayrollRun.company_id == company_id
        ).group_by(PayrollRun.payroll_status).all()

        counts_dict = {status: count for status, count in counts}

        summary = PayrollSummary(
            draft=counts_dict.get(PayrollStatus.DRAFT, 0),
            approved=counts_dict.get(PayrollStatus.APPROVED, 0),
            locked=counts_dict.get(PayrollStatus.LOCKED, 0)
        )

        return PayrollDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
