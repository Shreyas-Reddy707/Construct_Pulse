import { useCallback } from "react";
import { Users, HardHat, Building2 } from "lucide-react";
import { DashboardHeader } from "../components/DashboardHeader";
import { KpiCard } from "../components/KpiCard";
import { RecentActivityList } from "../components/RecentActivityList";
import { useDashboardMetrics } from "../hooks/useDashboardMetrics";
import { useRecentActivity } from "../hooks/useRecentActivity";

export function DashboardPage() {
  const { 
    data: metrics, 
    isLoading: metricsLoading,
    isRefetching: metricsRefetching,
    refetch: refetchMetrics,
    dataUpdatedAt: metricsUpdatedAt
  } = useDashboardMetrics();

  const {
    data: activity,
    isLoading: activityLoading,
    isRefetching: activityRefetching,
    refetch: refetchActivity,
    dataUpdatedAt: activityUpdatedAt
  } = useRecentActivity();

  const handleManualRefresh = useCallback(async () => {
    // Force a real network request by explicitly calling refetch
    await Promise.all([
      refetchMetrics(),
      refetchActivity()
    ]);
  }, [refetchMetrics, refetchActivity]);

  // Use the most recent timestamp between the two queries
  const lastUpdated = Math.max(metricsUpdatedAt || 0, activityUpdatedAt || 0) || undefined;
  const isRefetching = metricsRefetching || activityRefetching;

  return (
    <div className="space-y-6">
      <DashboardHeader 
        lastUpdated={lastUpdated} 
        onRefresh={handleManualRefresh} 
        isRefetching={isRefetching}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiCard
          title="Total Network Occupancy"
          value={metrics?.total_network_occupancy}
          icon={<Users className="w-5 h-5 text-muted-foreground" />}
          isLoading={metricsLoading}
        />
        <KpiCard
          title="Active Sites"
          value={metrics?.total_active_sites}
          icon={<Building2 className="w-5 h-5 text-muted-foreground" />}
          isLoading={metricsLoading}
        />
        <KpiCard
          title="Active Workforce"
          value={metrics?.total_active_workers}
          icon={<HardHat className="w-5 h-5 text-muted-foreground" />}
          isLoading={metricsLoading}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-4">
        <div className="lg:col-span-2 bg-card text-card-foreground shadow-sm border rounded-xl p-6 min-h-[300px] flex items-center justify-center">
          <p className="text-muted-foreground text-sm">Top Sites chart placeholder</p>
        </div>
        
        <div className="col-span-1 bg-card text-card-foreground shadow-sm border rounded-xl p-6">
          <h3 className="font-semibold mb-4 tracking-tight">Recent Activity</h3>
          <RecentActivityList 
            items={activity?.items} 
            isLoading={activityLoading} 
          />
        </div>
      </div>
    </div>
  );
}
