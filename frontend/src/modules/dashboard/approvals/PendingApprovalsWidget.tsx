import { usePendingApprovals } from "../hooks/useDashboardQueries";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Clock } from "lucide-react";

interface PendingApprovalsWidgetProps {
  className?: string;
}

export function PendingApprovalsWidget({ className }: PendingApprovalsWidgetProps) {
  const { data, isLoading, isError } = usePendingApprovals();

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <Skeleton className="h-6 w-1/3" />
          <Skeleton className="h-4 w-1/4 mt-2" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (isError || !data) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <div className="text-sm text-destructive">Failed to load pending approvals.</div>
        </CardContent>
      </Card>
    );
  }

  if (data.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Pending Approvals</CardTitle>
          <CardDescription>Action items requiring your attention</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-muted-foreground flex items-center gap-2">
            You are all caught up!
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={`border-l-4 border-l-amber-500 ${className}`}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-amber-600 dark:text-amber-500">Action Required</CardTitle>
            <CardDescription>Pending approvals blocking worker progress</CardDescription>
          </div>
          <Badge variant="outline" className="bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400">
            {data.length} Items
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((item) => (
            <div key={item.id} className="flex items-start justify-between border-b pb-4 last:border-0 last:pb-0">
              <div>
                <p className="font-medium text-sm">{item.description}</p>
                <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                  <span className="capitalize">{item.type}</span>
                  <span>•</span>
                  <span>{item.submitted_by}</span>
                </div>
              </div>
              <div className="flex items-center text-xs text-muted-foreground">
                <Clock className="mr-1 h-3 w-3" />
                {new Date(item.submitted_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
