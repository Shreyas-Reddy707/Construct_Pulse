import { useParams } from "react-router-dom";
import { DepartmentAttendanceLog } from "@/modules/attendance/components/DepartmentAttendanceLog";

export default function DepartmentAttendanceTab() {
  const { id } = useParams<{ id: string }>();

  if (!id) return null;

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Attendance Log</h3>
        <p className="text-sm text-muted-foreground">
          Historical attendance events across all sites for workers belonging to this department.
        </p>
      </div>
      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <DepartmentAttendanceLog departmentId={id} />
      </div>
    </div>
  );
}
