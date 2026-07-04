from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence

from app.models.models import (
    ComplianceReport, ComplianceReportSnapshot, ReportAuditLog,
    ReportStatus, ReportSource, ReportType
)
from app.schemas.schemas import (
    ReportGenerateRequest, ComplianceReportResponse, ComplianceReportSnapshotResponse,
    ReportDashboard, ReportSummary, AttendanceReportQuery
)
from app.services.attendance_reporting_service import AttendanceReportingService
from app.services.payroll_service import PayrollService

class ReportingService:
    """
    Public Service Contract:
    ReportingService is the exclusive public interface for the Reporting & Compliance Foundation.
    Future domains must consume ReportingService.
    Direct querying of Reporting ORM models (ComplianceReport, ComplianceReportSnapshot, ReportAuditLog) is forbidden.
    They remain internal implementation details.

    Reporting is a downstream read-model. It consumes certified projections only and never performs operational calculations.

    Lifecycle:
    GENERATED
        ↓
    ARCHIVED

    GENERATED:
    - Immutable snapshot created.
    - Available for viewing.
    - Historical baseline established.

    ARCHIVED:
    - Removed from active operational views.
    - Historical record retained.
    - Cannot be reopened.
    - Cannot be modified.
    """

    @classmethod
    def _generate_report_number(cls, db: Session) -> str:
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('compliance_report_number_seq')).scalar()
        return f"REP-{year}-{seq_val:06d}"

    @classmethod
    def _create_audit_log(
        cls, db: Session, compliance_report_id: str, report_version: int, audit_batch_id: str,
        old_status: Optional[ReportStatus], new_status: Optional[ReportStatus],
        performed_by: str, reason: str
    ):
        # Architectural Comment: ReportAuditLog is append-only. 
        # This guarantees an unbroken historical chain of compliance actions.
        # Note: Report viewing intentionally does not generate audit records to avoid operational bloat.
        audit = ReportAuditLog(
            compliance_report_id=compliance_report_id,
            report_version=report_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def _create_snapshot(cls, db: Session, compliance_report_id: str, snapshot_data: Dict[str, Any]):
        # Architectural Comment: Every snapshot is an immutable historical record.
        # Snapshots are never regenerated or synchronized with downstream domains.
        # Operational changes after report generation must never modify historical snapshots.
        # A new report generation always produces a brand-new snapshot.
        snapshot = ComplianceReportSnapshot(
            compliance_report_id=compliance_report_id,
            snapshot_data=snapshot_data
        )
        db.add(snapshot)

    @classmethod
    def _map_snapshot_to_dto(cls, snapshot: ComplianceReportSnapshot) -> ComplianceReportSnapshotResponse:
        return ComplianceReportSnapshotResponse(
            id=snapshot.id,
            compliance_report_id=snapshot.compliance_report_id,
            snapshot_data=snapshot.snapshot_data
        )

    @classmethod
    def _map_to_dto(cls, report: ComplianceReport, include_snapshot: bool = False) -> ComplianceReportResponse:
        snapshot_dto = None
        if include_snapshot and report.snapshot:
            snapshot_dto = cls._map_snapshot_to_dto(report.snapshot)
            
        return ComplianceReportResponse(
            id=report.id,
            company_id=report.company_id,
            site_id=report.site_id,
            report_number=report.report_number,
            report_type=report.report_type,
            report_status=report.report_status,
            report_source=report.report_source,
            report_version=report.report_version,
            generated_by=report.generated_by,
            generated_at=report.generated_at,
            archived_at=report.archived_at,
            snapshot=snapshot_dto
        )

    @classmethod
    def generate_report(cls, db: Session, company_id: str, current_user_id: str, payload: ReportGenerateRequest) -> ComplianceReportResponse:
        # Generate the root aggregate
        report_number = cls._generate_report_number(db)
        
        report = ComplianceReport(
            company_id=company_id,
            site_id=payload.site_id,
            report_number=report_number,
            report_type=payload.report_type,
            report_status=ReportStatus.GENERATED,
            report_source=ReportSource.SYSTEM,
            generated_by=current_user_id
        )
        db.add(report)
        db.flush()

        # Architectural Comment: Reporting consumes certified public reporting contracts exposed by downstream foundations.
        # Examples include Attendance Reporting, Occupancy, Payroll, Workforce Planning, Safety, Incident, Visitor, Emergency Muster, Notification.
        # Reporting depends only on stable public service interfaces and never on private helpers or ORM models.
        # This prevents coupling to operational schemas.
        snapshot_data = {}
        
        if payload.report_type == ReportType.PAYROLL_SUMMARY:
            # Consume Payroll Dashboard projection
            dashboard_dto = PayrollService.dashboard(db, company_id)
            snapshot_data = dashboard_dto.dict()
            snapshot_data["generated_at"] = snapshot_data["generated_at"].isoformat()
            
        elif payload.report_type == ReportType.ATTENDANCE_COMPLIANCE:
            # Consume Attendance Reporting projection
            query = AttendanceReportQuery(
                start_date=payload.parameters.get("start_date"),
                end_date=payload.parameters.get("end_date"),
                company_id=company_id,
                site_id=payload.site_id
            )
            report_dto = AttendanceReportingService.get_report(db, query)
            
            # Serialize for JSONB
            snapshot_data = {
                "report_id": report_dto.report_id,
                "generated_at": report_dto.generated_at.isoformat(),
                "metadata": report_dto.metadata.dict(),
                "rows": [r.dict() for r in report_dto.rows]
            }
            # Handle datetime serialization within rows if necessary
            for row in snapshot_data["rows"]:
                if row.get("check_in_time"): row["check_in_time"] = row["check_in_time"].isoformat()
                if row.get("check_out_time"): row["check_out_time"] = row["check_out_time"].isoformat()
        else:
            # Generic fallback for unhandled types
            snapshot_data = {"message": f"Report data for {payload.report_type.value} compiled successfully."}

        # Create immutable snapshot
        cls._create_snapshot(db, compliance_report_id=report.id, snapshot_data=snapshot_data)
        
        # Append audit log
        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            compliance_report_id=report.id,
            report_version=report.report_version,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=ReportStatus.GENERATED,
            performed_by=current_user_id,
            reason="Compliance report generated"
        )

        db.commit()
        db.refresh(report)
        return cls._map_to_dto(report, include_snapshot=True)

    @classmethod
    def archive(cls, db: Session, report_id: str, current_user_id: str) -> ComplianceReportResponse:
        report = db.query(ComplianceReport).filter(ComplianceReport.id == report_id).first()
        if not report:
            raise ValueError("Compliance report not found")
            
        if report.report_status != ReportStatus.GENERATED:
            raise ValueError("Only GENERATED reports can be ARCHIVED")
            
        old_status = report.report_status
        report.report_status = ReportStatus.ARCHIVED
        report.archived_at = datetime.now(timezone.utc)
        
        # Architectural Comment: report_version prepares for optimistic concurrency.
        # It increments ONLY when the report's own lifecycle changes.
        report.report_version += 1
        
        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            compliance_report_id=report.id,
            report_version=report.report_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=ReportStatus.ARCHIVED,
            performed_by=current_user_id,
            reason="Compliance report archived"
        )
        
        db.commit()
        db.refresh(report)
        return cls._map_to_dto(report, include_snapshot=False)

    @classmethod
    def list_reports(cls, db: Session, company_id: str, skip: int = 0, limit: int = 100) -> List[ComplianceReportResponse]:
        reports = db.query(ComplianceReport).filter(
            ComplianceReport.company_id == company_id
        ).order_by(ComplianceReport.generated_at.desc()).offset(skip).limit(limit).all()
        return [cls._map_to_dto(report, include_snapshot=False) for report in reports]

    @classmethod
    def get_snapshot(cls, db: Session, report_id: str, company_id: str) -> Optional[ComplianceReportResponse]:
        report = db.query(ComplianceReport).filter(
            ComplianceReport.id == report_id,
            ComplianceReport.company_id == company_id
        ).first()
        if report:
            return cls._map_to_dto(report, include_snapshot=True)
        return None

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> ReportDashboard:
        counts = db.query(
            ComplianceReport.report_status,
            func.count(ComplianceReport.id)
        ).filter(
            ComplianceReport.company_id == company_id
        ).group_by(ComplianceReport.report_status).all()
        
        counts_dict = {status: count for status, count in counts}
        
        summary = ReportSummary(
            generated=counts_dict.get(ReportStatus.GENERATED, 0),
            archived=counts_dict.get(ReportStatus.ARCHIVED, 0)
        )
        
        return ReportDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
