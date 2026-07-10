import { Link } from "react-router-dom";
import { User, Phone, Mail, AlertTriangle } from "lucide-react";
import type { WorkerDetail } from "../../types";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { Skeleton } from "@/components/ui/skeleton";

interface WorkerSidebarProps {
  worker?: WorkerDetail;
  isLoading: boolean;
}

export function WorkerSidebar({ worker, isLoading }: WorkerSidebarProps) {
  if (isLoading) {
    return (
      <div className="w-full lg:w-80 flex-shrink-0 space-y-6">
        <Skeleton className="h-48 w-full rounded-xl" />
        <Skeleton className="h-24 w-full rounded-xl" />
      </div>
    );
  }

  if (!worker) {
    return null;
  }

  const isSuspended = worker.status === "suspended";

  return (
    <div className={`w-full lg:w-80 flex-shrink-0 space-y-6 flex flex-col`}>
      <div className={`bg-card text-card-foreground shadow-sm border rounded-xl overflow-hidden ${isSuspended ? "border-red-500 ring-1 ring-red-500" : ""}`}>
        <div className="p-6 flex flex-col items-center text-center space-y-4">
          <div className="h-24 w-24 bg-muted rounded-full flex items-center justify-center">
            <User className="h-12 w-12 text-muted-foreground" />
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-tight">
              {worker.first_name} {worker.last_name}
            </h2>
            <p className="text-muted-foreground">{worker.role}</p>
          </div>
          <StatusBadgeCell 
            status={worker.status}
          />
        </div>
      </div>

      <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 space-y-4">
        <h3 className="font-semibold tracking-tight">Assignment</h3>
        <div className="space-y-3 text-sm">
          <div>
            <p className="text-muted-foreground">Contractor</p>
            <p className="font-medium">
              {/* Assuming we might have real IDs later, using `#` as placeholder for now */}
              <Link to={`/contractors/temp-id`} className="hover:underline text-primary" aria-label="View Contractor Details">
                {worker.contractor_name}
              </Link>
            </p>
          </div>
          <div>
            <p className="text-muted-foreground">Department</p>
            <p className="font-medium">
              <Link to={`/departments/temp-id`} className="hover:underline text-primary" aria-label="View Department Details">
                {worker.department_name}
              </Link>
            </p>
          </div>
        </div>
      </div>

      <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 space-y-4">
        <h3 className="font-semibold tracking-tight">Contact</h3>
        <div className="space-y-3 text-sm">
          <div className="flex items-center gap-2">
            <Phone className="h-4 w-4 text-muted-foreground" />
            <span>{worker.phone || "Not provided"}</span>
          </div>
          <div className="flex items-center gap-2">
            <Mail className="h-4 w-4 text-muted-foreground" />
            <span className="truncate">{worker.email || "Not provided"}</span>
          </div>
        </div>
      </div>

      {worker.emergency_contact && (
        <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 space-y-4 border-l-4 border-l-orange-500">
          <div className="flex items-center gap-2 text-orange-600">
            <AlertTriangle className="h-4 w-4" />
            <h3 className="font-semibold tracking-tight">Emergency Contact</h3>
          </div>
          <p className="text-sm">{worker.emergency_contact}</p>
        </div>
      )}
    </div>
  );
}
