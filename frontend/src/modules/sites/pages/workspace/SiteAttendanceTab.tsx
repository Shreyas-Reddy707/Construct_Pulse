import { useParams } from "react-router-dom";
import { SiteAttendanceLog } from "@/modules/attendance/components/SiteAttendanceLog";

export default function SiteAttendanceTab() {
  const { id } = useParams<{ id: string }>();

  if (!id) return null;

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Attendance Log</h3>
        <p className="text-sm text-muted-foreground">
          Historical log of all check-in and check-out events at this site.
        </p>
      </div>
      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <SiteAttendanceLog siteId={id} />
      </div>
    </div>
  );
}
