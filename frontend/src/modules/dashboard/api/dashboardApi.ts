import type { DashboardSummary, DashboardTrend, LiveOccupancy, PendingApproval } from "../types";

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummary> => {
    // Mocking response for MVP since backend might not have these specific endpoints fully wired for Dashboard yet
    // but assuming standard GET structure
    // const response = await apiClient.get<DashboardSummary>("/analytics/summary");
    // return response.data;
    
    // Simulate network delay for MVP demo
    return new Promise((resolve) => setTimeout(() => resolve({
      headcount: 142,
      occupancy: 85,
      today_hours: 1136,
      pending_approvals: 12
    }), 800));
  },

  getTrends: async (): Promise<DashboardTrend[]> => {
    return new Promise((resolve) => setTimeout(() => resolve([
      { date: "Mon", headcount: 120, occupancy: 70 },
      { date: "Tue", headcount: 135, occupancy: 80 },
      { date: "Wed", headcount: 140, occupancy: 82 },
      { date: "Thu", headcount: 138, occupancy: 81 },
      { date: "Fri", headcount: 142, occupancy: 85 },
    ]), 1500));
  },

  getLiveOccupancy: async (): Promise<LiveOccupancy> => {
    return new Promise((resolve) => setTimeout(() => resolve({
      site_id: "site-1",
      current_occupancy: 142,
      max_capacity: 200,
      status: "safe"
    }), 500));
  },

  getPendingApprovals: async (): Promise<PendingApproval[]> => {
    return new Promise((resolve) => setTimeout(() => resolve([
      { id: "1", type: "timesheet", description: "Timesheet - John Doe", submitted_by: "John Doe", submitted_at: "2026-07-09T10:00:00Z" },
      { id: "2", type: "registration", description: "New Worker Registration", submitted_by: "Jane Smith", submitted_at: "2026-07-09T09:30:00Z" },
      { id: "3", type: "incident", description: "Safety Incident Report", submitted_by: "Mike Johnson", submitted_at: "2026-07-09T08:15:00Z" },
    ]), 600));
  }
};
