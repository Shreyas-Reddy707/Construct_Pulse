import { useParams } from "react-router-dom";
import { WorkerAttendanceLog } from "@/modules/attendance/components/WorkerAttendanceLog";

export function WorkerAttendanceTab() {
  const { id } = useParams<{ id: string }>();

  if (!id) return null;

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Attendance History</h3>
        <p className="text-sm text-muted-foreground">
          Log of all check-in and check-out events for this worker across all sites.
        </p>
      </div>
      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <WorkerAttendanceLog workerId={id} />
      </div>
    </div>
  );
}
