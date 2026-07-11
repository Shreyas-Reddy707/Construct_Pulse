import { useOutletContext } from "react-router-dom";
import type { WorkerDetail } from "../../types";
import { Skeleton } from "@/components/ui/skeleton";
import { Calendar, Briefcase, Hash } from "lucide-react";

export function WorkerOverviewTab() {
  const { worker, isLoading } = useOutletContext<{ worker?: WorkerDetail, isLoading: boolean }>();

  if (isLoading) {
    return <div className="space-y-4"><Skeleton className="h-64 w-full" /></div>;
  }

  if (!worker) return null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left side: Core Employment Details */}
      <div className="lg:col-span-2 space-y-6">
        <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6">
          <h3 className="font-semibold tracking-tight text-lg mb-4">Employment Details</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="space-y-1">
              <div className="flex items-center text-muted-foreground mb-1 text-sm">
                <Hash className="w-4 h-4 mr-2" /> Worker ID
              </div>
              <p className="font-medium text-sm break-all">{worker.id}</p>
            </div>
            <div className="space-y-1">
              <div className="flex items-center text-muted-foreground mb-1 text-sm">
                <Calendar className="w-4 h-4 mr-2" /> Onboarded
              </div>
              <p className="font-medium text-sm">
                {new Intl.DateTimeFormat("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric"
                }).format(new Date(worker.created_at))}
              </p>
            </div>
            <div className="space-y-1">
              <div className="flex items-center text-muted-foreground mb-1 text-sm">
                <Briefcase className="w-4 h-4 mr-2" /> Role
              </div>
              <p className="font-medium text-sm">{worker.role}</p>
            </div>
            <div className="space-y-1">
              <div className="flex items-center text-muted-foreground mb-1 text-sm">
                <span className="w-4 h-4 mr-2 bg-muted rounded-full inline-block" /> Status
              </div>
              <p className="font-medium text-sm capitalize">{worker.status}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right side: Future Activity Timeline */}
      <div className="lg:col-span-1">
        <div className="bg-muted/50 border rounded-xl p-6 h-full min-h-[300px] flex flex-col items-center justify-center text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center">
            <Calendar className="w-6 h-6 text-muted-foreground" />
          </div>
          <div>
            <h4 className="font-medium">Activity Timeline</h4>
            <p className="text-sm text-muted-foreground max-w-[200px] mt-1">
              Timeline of status changes and check-ins will appear here in a future update.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
