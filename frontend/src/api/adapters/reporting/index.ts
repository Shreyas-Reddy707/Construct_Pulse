import type { 
  ComplianceReport, 
  ReportSnapshot, 
  ReportDashboard, 
  ReportType, 
  ReportStatus, 
  ReportSource 
} from "@/modules/reporting/types";

export interface BackendReportSnapshot {
  id: string;
  compliance_report_id: string;
  snapshot_data: Record<string, any>;
}

export interface BackendComplianceReport {
  id: string;
  company_id: string;
  site_id: string | null;
  report_number: string;
  report_type: ReportType;
  report_status: ReportStatus;
  report_source: ReportSource;
  report_version: number;
  generated_by: string;
  generated_at: string;
  archived_at: string | null;
  snapshot: BackendReportSnapshot | null;
}

export interface BackendReportSummary {
  generated: number;
  archived: number;
}

export interface BackendReportDashboard {
  report_id: string;
  generated_at: string;
  summary: BackendReportSummary;
}

export function mapReportSnapshot(dto: BackendReportSnapshot): ReportSnapshot {
  return {
    id: dto.id,
    complianceReportId: dto.compliance_report_id,
    snapshotData: dto.snapshot_data,
  };
}

export function mapComplianceReport(dto: BackendComplianceReport): ComplianceReport {
  return {
    id: dto.id,
    companyId: dto.company_id,
    siteId: dto.site_id,
    reportNumber: dto.report_number,
    reportType: dto.report_type,
    reportStatus: dto.report_status,
    reportSource: dto.report_source,
    reportVersion: dto.report_version,
    generatedBy: dto.generated_by,
    generatedAt: dto.generated_at,
    archivedAt: dto.archived_at,
    snapshot: dto.snapshot ? mapReportSnapshot(dto.snapshot) : null,
  };
}

export function mapReportDashboard(dto: BackendReportDashboard): ReportDashboard {
  return {
    reportId: dto.report_id,
    generatedAt: dto.generated_at,
    summary: {
      generated: dto.summary.generated,
      archived: dto.summary.archived,
    },
  };
}
