import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useGenerateReport } from "../hooks/useReports";
import type { ReportType } from "../types";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";

const REPORT_TYPES: { label: string; value: ReportType }[] = [
  { label: "Attendance Compliance", value: "ATTENDANCE_COMPLIANCE" },
  { label: "Payroll Summary", value: "PAYROLL_SUMMARY" },
  { label: "Safety Summary", value: "SAFETY_SUMMARY" },
  { label: "Incident Summary", value: "INCIDENT_SUMMARY" },
  { label: "Occupancy Summary", value: "OCCUPANCY_SUMMARY" },
];

export function GenerateReportDialog({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [reportType, setReportType] = useState<ReportType>("ATTENDANCE_COMPLIANCE");
  const { mutateAsync, isPending } = useGenerateReport();

  const handleGenerate = async () => {
    try {
      await mutateAsync({
        report_type: reportType,
        parameters: {}, // Default empty for MVP
      });
      toast.success("Report generated successfully");
      setOpen(false);
    } catch (error) {
      toast.error("Failed to generate report");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Generate New Report</DialogTitle>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label>Report Type</Label>
            <Select value={reportType} onValueChange={(val) => setReportType(val as ReportType)}>
              <SelectTrigger>
                <SelectValue placeholder="Select report type" />
              </SelectTrigger>
              <SelectContent>
                {REPORT_TYPES.map((type) => (
                  <SelectItem key={type.value} value={type.value}>
                    {type.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button onClick={handleGenerate} disabled={isPending}>
            {isPending ? "Generating..." : "Generate"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
