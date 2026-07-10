import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DashboardHeaderProps {
  lastUpdated?: number;
  onRefresh: () => void;
  isRefetching: boolean;
}

export function DashboardHeader({ lastUpdated, onRefresh, isRefetching }: DashboardHeaderProps) {
  const formattedTime = lastUpdated 
    ? new Date(lastUpdated).toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      })
    : "—";

  return (
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 pb-4 border-b">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Operations Dashboard</h1>
        <div className="flex items-center gap-2 mt-2">
          {/* Live pulsing indicator */}
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
          </span>
          <span className="text-sm text-muted-foreground" aria-live="polite">
            Live • Last Updated: {formattedTime}
          </span>
        </div>
      </div>
      
      <Button 
        variant="outline" 
        size="sm" 
        onClick={onRefresh}
        disabled={isRefetching}
        className="w-full sm:w-auto"
      >
        <RefreshCw className={`mr-2 h-4 w-4 ${isRefetching ? "animate-spin" : ""}`} />
        Refresh Now
      </Button>
    </div>
  );
}
