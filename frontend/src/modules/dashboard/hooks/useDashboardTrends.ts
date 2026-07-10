import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboardApi";
import { DASHBOARD_CONFIG } from "../config";
import { dashboardKeys } from "./useDashboardMetrics";

export function useDashboardTrends() {
  return useQuery({
    queryKey: [...dashboardKeys.all, "trends"] as const,
    queryFn: () => dashboardApi.getTrends(),
    refetchInterval: DASHBOARD_CONFIG.POLLING_INTERVAL_MS,
    refetchIntervalInBackground: false,
  });
}
