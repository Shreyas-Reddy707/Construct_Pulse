import { ArrowLeft, User, Phone, Mail, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";
import type { WorkerDetail } from "../../types";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { Skeleton } from "@/components/ui/skeleton";
import { WorkerActions } from "./WorkerActions";

interface WorkerWorkspaceHeaderProps {
  worker?: WorkerDetail;
  isLoading: boolean;
}

export function WorkerWorkspaceHeader({ worker, isLoading }: WorkerWorkspaceHeaderProps) {
  if (isLoading) {
    return (
      <div className="sticky top-0 z-10 bg-background border-b shadow-sm w-full p-6">
        <Skeleton className="h-16 w-full" />
      </div>
    );
  }

  if (!worker) return null;

  const isSuspended = worker.status === "suspended";

  return (
    <div className={`sticky top-0 z-10 bg-background border-b shadow-sm w-full ${isSuspended ? "border-b-destructive/50 bg-destructive/5" : ""}`}>
      <div className="flex flex-col md:flex-row md:items-center justify-between p-6 gap-6">
        {/* Left: Identity & Navigation */}
        <div className="flex items-start gap-4">
          <div className="hidden sm:flex h-12 w-12 rounded-xl bg-primary/10 items-center justify-center text-primary flex-shrink-0">
            <User className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
              <Link to="/workers" className="hover:text-foreground flex items-center transition-colors">
                <ArrowLeft className="h-4 w-4 mr-1" />
                Workers
              </Link>
              <span>/</span>
              <span>{worker.id}</span>
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold tracking-tight">
                {worker.first_name} {worker.last_name}
              </h1>
              <StatusBadgeCell status={worker.status} />
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
              <span className="font-medium text-foreground">{worker.role}</span>
              <span>•</span>
              <Link to={`/contractors/temp-id`} className="hover:underline text-primary" aria-label="View Contractor Details">
                {worker.contractor_name}
              </Link>
              <span>•</span>
              <Link to={`/departments/temp-id`} className="hover:underline text-primary" aria-label="View Department Details">
                {worker.department_name}
              </Link>
            </div>
          </div>
        </div>

        {/* Middle: Contact Info */}
        <div className="flex-shrink-0 bg-card border rounded-xl p-4 flex flex-col gap-2 shadow-sm min-w-[200px]">
          <div className="flex items-center gap-2 text-sm">
            <Phone className="h-4 w-4 text-muted-foreground" />
            <span>{worker.phone || "No phone provided"}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Mail className="h-4 w-4 text-muted-foreground" />
            <span className="truncate">{worker.email || "No email provided"}</span>
          </div>
          {worker.emergency_contact && (
            <div className="flex items-center gap-2 text-sm text-orange-600 mt-1">
              <AlertTriangle className="h-4 w-4" />
              <span className="truncate" title={worker.emergency_contact}>{worker.emergency_contact}</span>
            </div>
          )}
        </div>

        {/* Far Right: Actions */}
        <div className="flex items-center">
          <WorkerActions worker={worker} />
        </div>
      </div>
    </div>
  );
}
