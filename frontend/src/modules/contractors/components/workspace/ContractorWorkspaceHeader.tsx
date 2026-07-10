import { ArrowLeft, HardHat, Mail, Phone, User } from "lucide-react";
import { Link } from "react-router-dom";
import type { ContractorDetail } from "../../types";
import { StatusBadgeCell } from "@/components/data-table/cells/StatusBadgeCell";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";

interface ContractorWorkspaceHeaderProps {
  contractor?: ContractorDetail;
  isLoading: boolean;
}

export function ContractorWorkspaceHeader({ contractor, isLoading }: ContractorWorkspaceHeaderProps) {
  if (isLoading) {
    return (
      <div className="bg-background border-b shadow-sm w-full p-6">
        <Skeleton className="h-24 w-full" />
      </div>
    );
  }

  if (!contractor) return null;

  return (
    <div className="bg-background border-b shadow-sm w-full">
      <div className="flex flex-col xl:flex-row xl:items-start justify-between p-6 gap-6">
        
        {/* Left: Identity & Navigation */}
        <div className="flex items-start gap-4">
          <div className="hidden sm:flex h-16 w-16 rounded-xl bg-primary/10 items-center justify-center text-primary flex-shrink-0">
            <HardHat className="h-8 w-8" />
          </div>
          <div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
              <Link to="/contractors" className="hover:text-foreground flex items-center transition-colors">
                <ArrowLeft className="h-4 w-4 mr-1" />
                Contractors
              </Link>
              <span>/</span>
              <span>{contractor.id.split("-")[0]}</span>
            </div>
            
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="text-3xl font-bold tracking-tight">{contractor.name}</h1>
              <StatusBadgeCell status={contractor.operational_status} />
              {contractor.compliance_status === "compliant" && (
                <Badge variant="default" className="bg-green-600 hover:bg-green-700">Compliant</Badge>
              )}
              {contractor.compliance_status === "non_compliant" && (
                <Badge variant="destructive">Non-Compliant</Badge>
              )}
              {contractor.compliance_status === "review_pending" && (
                <Badge variant="secondary">Review Pending</Badge>
              )}
            </div>

            {/* Contact Information */}
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mt-3">
              <div className="flex items-center gap-1.5 text-foreground font-medium">
                <User className="h-4 w-4" />
                <span>{contractor.primary_contact_name}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Phone className="h-4 w-4" />
                <span>{contractor.primary_contact_phone}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Mail className="h-4 w-4" />
                <span>{contractor.primary_contact_email}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Operational KPIs */}
        <div className="flex-shrink-0 grid grid-cols-2 sm:flex items-stretch gap-4">
          <div className="bg-card border rounded-xl p-4 min-w-[120px]">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Total Workers
            </p>
            <p className="text-2xl font-bold">{contractor.total_workers}</p>
          </div>
          
          <div className="bg-card border rounded-xl p-4 min-w-[120px]">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Active Workers
            </p>
            <p className="text-2xl font-bold text-primary">{contractor.active_workers}</p>
          </div>

          <div className="bg-card border rounded-xl p-4 min-w-[120px]">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
              Active Sites
            </p>
            <p className="text-2xl font-bold">{contractor.active_sites}</p>
          </div>
        </div>

      </div>
    </div>
  );
}
