export interface DashboardMetricsResponse {
  total_network_occupancy: number;
  total_active_sites: number;
  total_active_workers: number;
}

export interface RecentActivityItem {
  id: string;
  worker_name: string;
  site_name: string;
  action: "check_in" | "check_out";
  timestamp: string; // ISO string
}

export interface RecentActivityResponse {
  items: RecentActivityItem[];
}

export interface DashboardTrendItem {
  date: string;
  headcount: number;
  hours: number;
  corrections: number;
}
