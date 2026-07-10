import { apiClient } from "@/api/client";
import type { DashboardMetricsResponse, RecentActivityResponse, DashboardTrendItem } from "../types";
import type { 
  BackendDashboardSummary, 
  BackendRecentActivity,
  BackendDashboardTrend
} from "@/api/adapters/dashboard";
import {
  mapDashboardMetrics, 
  mapRecentActivity,
  mapDashboardTrends
} from "@/api/adapters/dashboard";

const DEFAULT_LOOKBACK_DAYS = 7;

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

  getTrends: async (): Promise<DashboardTrendItem[]> => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(endDate.getDate() - DEFAULT_LOOKBACK_DAYS);

    const response = await apiClient.get<BackendDashboardTrend[]>("/dashboard/trends", {
      params: {
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
      },
    });

    return response.data.map(mapDashboardTrends);
  },
};
