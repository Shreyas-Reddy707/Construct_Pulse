import type { RecentActivityItem } from "../types";
import { Skeleton } from "@/components/ui/skeleton";

interface RecentActivityListProps {
  items?: RecentActivityItem[];
  isLoading?: boolean;
}

// Simple relative time formatter for display (Presentation only)
function getRelativeTime(isoString: string): string {
  const diff = Date.now() - new Date(isoString).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function RecentActivityList({ items, isLoading }: RecentActivityListProps) {
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex items-center gap-4">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-4 w-[200px]" />
              <Skeleton className="h-3 w-[150px]" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!items || items.length === 0) {
    return <div className="text-sm text-muted-foreground py-8 text-center">No recent activity found.</div>;
  }

  return (
    <div className="space-y-6">
      {items.map((item) => (
        <div key={item.id} className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div 
              className={`w-2 h-2 rounded-full ${
                item.action === "check_in" ? "bg-green-500" : "bg-gray-400"
              }`} 
              aria-hidden="true"
            />
            <div className="space-y-1">
              <p className="text-sm font-medium leading-none">
                {item.worker_name}
              </p>
              <p className="text-sm text-muted-foreground">
                {item.action === "check_in" ? "Checked in to" : "Checked out of"} {item.site_name}
              </p>
            </div>
          </div>
          <div className="text-sm text-muted-foreground tabular-nums">
            {getRelativeTime(item.timestamp)}
          </div>
        </div>
      ))}
    </div>
  );
}
