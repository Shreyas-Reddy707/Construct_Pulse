export type ReportType = 
  | "ATTENDANCE_COMPLIANCE" 
  | "PAYROLL_SUMMARY" 
  | "SAFETY_SUMMARY" 
  | "INCIDENT_SUMMARY" 
  | "OCCUPANCY_SUMMARY";

export type ReportStatus = "GENERATED" | "ARCHIVED";
export type ReportSource = "MANUAL" | "SYSTEM";

export interface ReportSummary {
  generated: number;
  archived: number;
}

export interface ReportDashboard {
  reportId: string;
  generatedAt: string;
  summary: ReportSummary;
}

export interface ReportSnapshot {
  id: string;
  complianceReportId: string;
  snapshotData: Record<string, any>;
}

export interface ComplianceReport {
  id: string;
  companyId: string;
  siteId: string | null;
  reportNumber: string;
  reportType: ReportType;
  reportStatus: ReportStatus;
  reportSource: ReportSource;
  reportVersion: number;
  generatedBy: string;
  generatedAt: string;
  archivedAt: string | null;
  snapshot: ReportSnapshot | null;
}

export interface GenerateReportPayload {
  report_type: ReportType;
  site_id?: string;
  parameters: Record<string, any>;
}
