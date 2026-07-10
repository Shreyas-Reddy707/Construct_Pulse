import { apiClient } from "@/api/client";
import type { DashboardMetricsResponse, RecentActivityResponse } from "../types";
import type { 
  BackendDashboardSummary, 
  BackendRecentActivity
} from "@/api/adapters/dashboard";
import {
  mapDashboardMetrics, 
  mapRecentActivity 
} from "@/api/adapters/dashboard";

export const dashboardApi = {
  getMetrics: async (): Promise<DashboardMetricsResponse> => {
    // We can call /dashboard/metrics (which was aliased to /summary in the backend)
    const response = await apiClient.get<BackendDashboardSummary>("/dashboard/metrics");
    return mapDashboardMetrics(response.data);
  },
  
  getRecentActivity: async (): Promise<RecentActivityResponse> => {
    // Backend returns { items: [...] } so we just map the items array
    const response = await apiClient.get<{ items: BackendRecentActivity[] }>("/dashboard/recent-activity");
    return {
      items: response.data.items.map(mapRecentActivity),
    };
  },
};
