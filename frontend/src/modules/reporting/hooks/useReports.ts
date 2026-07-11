import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { reportingApi } from "../api/reportingApi";
import { useSearchParams } from "react-router-dom";
import type { GenerateReportPayload, ComplianceReport } from "../types";

export const reportKeys = {
  all: ["reports"] as const,
  lists: () => [...reportKeys.all, "list"] as const,
  list: (filters: Record<string, any>) => [...reportKeys.lists(), filters] as const,
  details: () => [...reportKeys.all, "detail"] as const,
  detail: (id: string) => [...reportKeys.details(), id] as const,
  dashboard: () => [...reportKeys.all, "dashboard"] as const,
};

export function useReports() {
  const [searchParams] = useSearchParams();
  
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  return useQuery({
    queryKey: reportKeys.list(params),
    queryFn: () => reportingApi.listReports(params),
    staleTime: 60 * 1000,
  });
}

export function useReport(reportId: string) {
  return useQuery({
    queryKey: reportKeys.detail(reportId),
    queryFn: () => reportingApi.getReport(reportId),
    enabled: !!reportId,
    staleTime: 5 * 60 * 1000,
  });
}

export function useReportingDashboard() {
  return useQuery({
    queryKey: reportKeys.dashboard(),
    queryFn: () => reportingApi.getDashboard(),
    staleTime: 60 * 1000,
  });
}

export function useGenerateReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: GenerateReportPayload) => reportingApi.generateReport(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reportKeys.lists() });
      queryClient.invalidateQueries({ queryKey: reportKeys.dashboard() });
    },
  });
}

export function useArchiveReport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (reportId: string) => reportingApi.archiveReport(reportId),
    onSuccess: (data: ComplianceReport) => {
      queryClient.invalidateQueries({ queryKey: reportKeys.detail(data.id) });
      queryClient.invalidateQueries({ queryKey: reportKeys.lists() });
      queryClient.invalidateQueries({ queryKey: reportKeys.dashboard() });
    },
  });
}
