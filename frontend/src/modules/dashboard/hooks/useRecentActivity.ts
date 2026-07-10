import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboardApi";
import { DASHBOARD_CONFIG } from "../config";
import { dashboardKeys } from "./useDashboardMetrics";

export function useRecentActivity() {
  return useQuery({
    queryKey: dashboardKeys.recentActivity(),
    queryFn: () => dashboardApi.getRecentActivity(),
    refetchInterval: DASHBOARD_CONFIG.POLLING_INTERVAL_MS,
    refetchIntervalInBackground: false,
  });
}
