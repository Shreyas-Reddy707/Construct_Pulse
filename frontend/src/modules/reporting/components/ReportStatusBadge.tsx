import { Badge } from "@/components/ui/badge";
import type { ReportStatus } from "../types";

export function ReportStatusBadge({ status }: { status: ReportStatus }) {
  if (status === "ARCHIVED") {
    return <Badge variant="secondary">Archived</Badge>;
  }
  return <Badge variant="default">Generated</Badge>;
}
