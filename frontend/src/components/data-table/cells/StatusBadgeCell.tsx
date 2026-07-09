import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface StatusBadgeCellProps {
  status: string;
  config?: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }>;
}

export function StatusBadgeCell({ status, config }: StatusBadgeCellProps) {
  const normalizedStatus = status.toLowerCase();
  
  const defaultConfig: Record<string, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
    active: { label: "Active", variant: "default" },
    suspended: { label: "Suspended", variant: "destructive" },
    pending: { label: "Pending", variant: "secondary" },
    inactive: { label: "Inactive", variant: "outline" },
  };

  const activeConfig = config || defaultConfig;
  const match = activeConfig[normalizedStatus] || { label: status, variant: "outline" };

  return (
    <Badge variant={match.variant} className={cn(
      match.variant === "default" && "bg-emerald-500 hover:bg-emerald-600 text-white",
      match.variant === "secondary" && "bg-amber-500 hover:bg-amber-600 text-white"
    )}>
      {match.label}
    </Badge>
  );
}
