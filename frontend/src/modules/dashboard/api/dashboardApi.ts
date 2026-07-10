import { apiClient } from "@/api/client";
import type { DashboardMetricsResponse, RecentActivityResponse } from "../types";

export const dashboardApi = {
  getMetrics: async (): Promise<DashboardMetricsResponse> => {
    const response = await apiClient.get<DashboardMetricsResponse>("/dashboard/metrics");
    return response.data;
  },
  
  getRecentActivity: async (): Promise<RecentActivityResponse> => {
    const response = await apiClient.get<RecentActivityResponse>("/dashboard/recent-activity");
    return response.data;
  },
};
