import { useDashboardSummary } from "../hooks/useDashboardQueries";
import { StatCard, StatCardSkeleton } from "../ui/StatCard";
import { Users, Clock, AlertCircle, Calendar } from "lucide-react";

export function SummaryCardsWidget() {
  const { data, isLoading, isError } = useDashboardSummary();

  if (isLoading) {
    return (
      <>
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
      </>
    );
  }

  if (isError || !data) {
    return (
      <div className="col-span-1 md:col-span-2 lg:col-span-4 p-4 text-center text-sm text-destructive border border-destructive/20 rounded-md bg-destructive/10">
        Failed to load dashboard summary.
      </div>
    );
  }

  return (
    <>
      <StatCard
        title="Current Headcount"
        value={data.headcount}
        icon={<Users size={16} />}
        description="Workers currently on site"
      />
      <StatCard
        title="Total Occupancy"
        value={`${data.occupancy}%`}
        icon={<AlertCircle size={16} />}
        description="Of maximum capacity"
      />
      <StatCard
        title="Today's Hours"
        value={data.today_hours}
        icon={<Clock size={16} />}
        description="Total hours logged today"
      />
      <StatCard
        title="Pending Approvals"
        value={data.pending_approvals}
        icon={<Calendar size={16} />}
        description="Awaiting review"
      />
    </>
  );
}
