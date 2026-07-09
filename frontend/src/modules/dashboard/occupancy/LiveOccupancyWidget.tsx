import { useLiveOccupancy } from "../hooks/useDashboardQueries";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Activity } from "lucide-react";

interface LiveOccupancyWidgetProps {
  className?: string;
}

export function LiveOccupancyWidget({ className }: LiveOccupancyWidgetProps) {
  const { data, isLoading, isError } = useLiveOccupancy();

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <Skeleton className="h-6 w-1/2" />
          <Skeleton className="h-4 w-1/3 mt-2" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-20 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (isError || !data) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="text-sm text-destructive">Failed to load live occupancy.</div>
        </CardContent>
      </Card>
    );
  }

  const occupancyPercentage = Math.round((data.current_occupancy / data.max_capacity) * 100);
  
  let statusColor = "bg-emerald-500";
  if (data.status === "warning") statusColor = "bg-amber-500";
  if (data.status === "critical") statusColor = "bg-destructive";

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-muted-foreground" />
              Live Occupancy
            </CardTitle>
            <CardDescription>Real-time site capacity</CardDescription>
          </div>
          <div className="text-right">
            <span className="text-2xl font-bold">{occupancyPercentage}%</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>{data.current_occupancy} present</span>
            <span>{data.max_capacity} max</span>
          </div>
          <div className="h-4 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className={`h-full transition-all duration-500 ease-in-out ${statusColor}`}
              style={{ width: `${Math.min(occupancyPercentage, 100)}%` }}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
