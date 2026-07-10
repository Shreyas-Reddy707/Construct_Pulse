import { ArrowLeft, Mail, Network, Phone, User } from "lucide-react";
import { Link } from "react-router-dom";
import type { DepartmentDetail } from "../../types";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { Skeleton } from "@/components/ui/skeleton";

interface DepartmentWorkspaceHeaderProps {
  department?: DepartmentDetail;
  isLoading: boolean;
}

export function DepartmentWorkspaceHeader({ department, isLoading }: DepartmentWorkspaceHeaderProps) {
  if (isLoading) {
    return (
      <div className="bg-background border-b shadow-sm w-full p-6">
        <Skeleton className="h-24 w-full" />
      </div>
    );
  }

  if (!department) return null;

  return (
    <div className="bg-background border-b shadow-sm w-full">
      <div className="flex flex-col xl:flex-row xl:items-start justify-between p-6 gap-6">
        
        {/* Left: Identity & Navigation */}
        <div className="flex items-start gap-4">
          <div className="hidden sm:flex h-16 w-16 rounded-xl bg-primary/10 items-center justify-center text-primary flex-shrink-0">
            <Network className="h-8 w-8" />
          </div>
          <div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
              <Link to="/departments" className="hover:text-foreground flex items-center transition-colors">
                <ArrowLeft className="h-4 w-4 mr-1" />
                Departments
              </Link>
              <span>/</span>
              <span>{department.department_code}</span>
            </div>
            
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="text-3xl font-bold tracking-tight">{department.name}</h1>
              <StatusBadgeCell status={department.status} />
            </div>

            {/* Leadership Information */}
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mt-3">
              <div className="flex items-center gap-1.5 text-foreground font-medium">
                <User className="h-4 w-4" />
                <span>Head: {department.head_name}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Phone className="h-4 w-4" />
                <span>{department.head_phone}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Mail className="h-4 w-4" />
                <span>{department.head_email}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Operational KPIs */}
        <div className="flex-shrink-0 grid grid-cols-2 items-stretch gap-4">
          <div className="bg-card border rounded-xl p-4 min-w-[120px]">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Total Personnel
            </p>
            <p className="text-2xl font-bold text-primary">{department.total_workers}</p>
          </div>
          
          <div className="bg-card border rounded-xl p-4 min-w-[120px]">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Active Sites
            </p>
            <p className="text-2xl font-bold">{department.active_sites}</p>
          </div>
        </div>

      </div>
    </div>
  );
}
