import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../api/dashboardApi";

export const dashboardKeys = {
  all: ["dashboard"] as const,
  summary: () => [...dashboardKeys.all, "summary"] as const,
  trends: () => [...dashboardKeys.all, "trends"] as const,
  occupancy: () => [...dashboardKeys.all, "occupancy"] as const,
  approvals: () => [...dashboardKeys.all, "approvals"] as const,
};

export function useDashboardSummary() {
  return useQuery({
    queryKey: dashboardKeys.summary(),
    queryFn: dashboardApi.getSummary,
    staleTime: 60 * 1000, // 60 seconds
  });
}

export function useDashboardTrends() {
  return useQuery({
    queryKey: dashboardKeys.trends(),
    queryFn: dashboardApi.getTrends,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useLiveOccupancy() {
  return useQuery({
    queryKey: dashboardKeys.occupancy(),
    queryFn: dashboardApi.getLiveOccupancy,
    staleTime: 15 * 1000, // 15 seconds
  });
}

export function usePendingApprovals() {
  return useQuery({
    queryKey: dashboardKeys.approvals(),
    queryFn: dashboardApi.getPendingApprovals,
    staleTime: 30 * 1000, // 30 seconds
  });
}
