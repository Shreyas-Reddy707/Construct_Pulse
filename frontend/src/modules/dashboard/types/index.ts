export interface DashboardSummary {
  headcount: number;
  occupancy: number;
  today_hours: number;
  pending_approvals: number;
}

export interface DashboardTrend {
  date: string;
  headcount: number;
  occupancy: number;
}

export interface LiveOccupancy {
  site_id: string;
  current_occupancy: number;
  max_capacity: number;
  status: "safe" | "warning" | "critical";
}

export interface PendingApproval {
  id: string;
  type: "timesheet" | "registration" | "incident";
  description: string;
  submitted_by: string;
  submitted_at: string;
}
