import type { DashboardMetricsResponse, RecentActivityItem } from "@/modules/dashboard/types";

export interface BackendDashboardSummary {
  total_workers?: number;
  active_sites?: number;
  workers_on_site?: number;
  workers_present_today?: number;
  attendance_rate?: number;
  average_shift_duration?: number;
  attendance_corrections?: number;
  total_completed_shifts?: number;
}

export interface BackendRecentActivity {
  id: string;
  worker_name: string;
  site_name: string;
  action: string;
  timestamp: string;
}

export function mapDashboardMetrics(backendSummary: BackendDashboardSummary): DashboardMetricsResponse {
  return {
    total_network_occupancy: backendSummary.workers_on_site || 0,
    total_active_sites: backendSummary.active_sites || 0,
    total_active_workers: backendSummary.total_workers || 0,
  };
}

export function mapRecentActivity(backendActivity: BackendRecentActivity): RecentActivityItem {
  return {
    id: backendActivity.id,
    worker_name: backendActivity.worker_name,
    site_name: backendActivity.site_name,
    action: (backendActivity.action === "check_in" || backendActivity.action === "check_out") 
      ? backendActivity.action 
      : "check_in",
    timestamp: backendActivity.timestamp,
  };
}
