import type { ReactNode } from "react";
import { Skeleton } from "@/components/ui/skeleton";

interface KpiCardProps {
  title: string;
  value?: number | string;
  icon: ReactNode;
  subtitle?: string;
  isLoading?: boolean;
}

export function KpiCard({ title, value, icon, subtitle, isLoading }: KpiCardProps) {
  return (
    <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-6 flex flex-col justify-between">
      <div className="flex flex-row items-center justify-between pb-2 space-y-0">
        <h3 className="tracking-tight text-sm font-medium">{title}</h3>
        <div className="text-muted-foreground">{icon}</div>
      </div>
      <div>
        {isLoading ? (
          <Skeleton className="h-8 w-16 mb-1" />
        ) : (
          <div className="text-2xl font-bold tabular-nums">
            {value !== undefined ? value : "—"}
          </div>
        )}
        {subtitle && <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}
