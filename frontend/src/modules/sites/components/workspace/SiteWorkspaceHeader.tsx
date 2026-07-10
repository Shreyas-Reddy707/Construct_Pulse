import { ArrowLeft, Building2, User } from "lucide-react";
import { Link } from "react-router-dom";
import type { SiteDetail } from "../../types";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { Skeleton } from "@/components/ui/skeleton";

interface SiteWorkspaceHeaderProps {
  site?: SiteDetail;
  isLoading: boolean;
}

export function SiteWorkspaceHeader({ site, isLoading }: SiteWorkspaceHeaderProps) {
  if (isLoading) {
    return (
      <div className="sticky top-0 z-10 bg-background border-b shadow-sm w-full p-6">
        <Skeleton className="h-16 w-full" />
      </div>
    );
  }

  if (!site) return null;

  return (
    <div className="sticky top-0 z-10 bg-background border-b shadow-sm w-full">
      <div className="flex flex-col md:flex-row md:items-center justify-between p-6 gap-6">
        {/* Left: Identity & Navigation */}
        <div className="flex items-start gap-4">
          <div className="hidden sm:flex h-12 w-12 rounded-xl bg-primary/10 items-center justify-center text-primary flex-shrink-0">
            <Building2 className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
              <Link to="/sites" className="hover:text-foreground flex items-center transition-colors">
                <ArrowLeft className="h-4 w-4 mr-1" />
                Sites
              </Link>
              <span>/</span>
              <span>{site.code}</span>
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold tracking-tight">{site.name}</h1>
              <StatusBadgeCell status={site.status} />
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
              <User className="h-4 w-4" />
              <span>Project Manager: {site.project_manager_name}</span>
            </div>
          </div>
        </div>

        {/* Right: Live Occupancy KPI */}
        <div className="flex-shrink-0 bg-card border rounded-xl p-4 flex items-center gap-6 shadow-sm">
          <div>
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Live Occupancy
            </p>
            <div className="flex items-baseline gap-2" aria-live="polite">
              <span className="text-3xl font-bold">{site.current_occupancy}</span>
              <span className="text-muted-foreground font-medium">/ {site.max_occupancy}</span>
            </div>
          </div>
          <div className="h-12 w-px bg-border hidden sm:block"></div>
          <div className="hidden sm:block text-right">
            <p className="text-sm text-muted-foreground">Capacity</p>
            <p className="font-medium">
              {Math.round((site.current_occupancy / site.max_occupancy) * 100)}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
