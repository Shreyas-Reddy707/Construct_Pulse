import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboardApi";
import { DASHBOARD_CONFIG } from "../config";

export const dashboardKeys = {
  all: ["dashboard"] as const,
  metrics: () => [...dashboardKeys.all, "metrics"] as const,
  recentActivity: () => [...dashboardKeys.all, "recentActivity"] as const,
};

export function useDashboardMetrics() {
  return useQuery({
    queryKey: dashboardKeys.metrics(),
    queryFn: () => dashboardApi.getMetrics(),
    refetchInterval: DASHBOARD_CONFIG.POLLING_INTERVAL_MS,
    refetchIntervalInBackground: false,
  });
}
