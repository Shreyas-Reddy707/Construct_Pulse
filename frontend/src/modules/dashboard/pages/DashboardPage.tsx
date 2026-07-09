import { SummaryCardsWidget } from "../summary/SummaryCardsWidget";
import { PendingApprovalsWidget } from "../approvals/PendingApprovalsWidget";
import { LiveOccupancyWidget } from "../occupancy/LiveOccupancyWidget";
import { TrendWidget } from "../trends/TrendWidget";

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Overview of your site operations and pending items.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Top Priority Action Items */}
        <PendingApprovalsWidget className="col-span-1 md:col-span-2 lg:col-span-4" />
        
        {/* Core KPIs */}
        <SummaryCardsWidget />
        
        {/* Secondary: Live Status & Trends */}
        <LiveOccupancyWidget className="col-span-1 md:col-span-1 lg:col-span-2" />
        <TrendWidget className="col-span-1 md:col-span-2 lg:col-span-4" />
      </div>
    </div>
  );
}
