import { apiClient } from "@/api/client";
import type { 
  ComplianceReport, 
  GenerateReportPayload, 
  ReportDashboard 
} from "../types";
import { 
  mapComplianceReport, 
  mapReportDashboard,
  type BackendComplianceReport,
  type BackendReportDashboard
} from "@/api/adapters/reporting";

export const reportingApi = {
  generateReport: async (payload: GenerateReportPayload): Promise<ComplianceReport> => {
    const response = await apiClient.post<BackendComplianceReport>("/reporting/generate", payload);
    return mapComplianceReport(response.data);
  },

  archiveReport: async (reportId: string): Promise<ComplianceReport> => {
    const response = await apiClient.post<BackendComplianceReport>(`/reporting/${reportId}/archive`);
    return mapComplianceReport(response.data);
  },

  listReports: async (params: Record<string, string | null> = {}): Promise<ComplianceReport[]> => {
    const { serializeQueryParams } = await import("@/api/utils");
    const searchParams = serializeQueryParams(params);
    const response = await apiClient.get<BackendComplianceReport[]>(`/reporting?${searchParams.toString()}`);
    return response.data.map(mapComplianceReport);
  },

  getDashboard: async (): Promise<ReportDashboard> => {
    const response = await apiClient.get<BackendReportDashboard>("/reporting/dashboard");
    return mapReportDashboard(response.data);
  },

  getReport: async (reportId: string): Promise<ComplianceReport> => {
    const response = await apiClient.get<BackendComplianceReport>(`/reporting/${reportId}`);
    return mapComplianceReport(response.data);
  },
};
