import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useArchiveReport } from "../hooks/useReports";
import { toast } from "sonner";

interface ArchiveReportDialogProps {
  reportId: string;
  children: React.ReactNode;
  disabled?: boolean;
}

export function ArchiveReportDialog({ reportId, children, disabled }: ArchiveReportDialogProps) {
  const [open, setOpen] = useState(false);
  const { mutateAsync, isPending } = useArchiveReport();

  const handleArchive = async () => {
    try {
      await mutateAsync(reportId);
      toast.success("Report archived successfully");
      setOpen(false);
    } catch (error) {
      toast.error("Failed to archive report");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild disabled={disabled || isPending}>
        {children}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Archive Report?</DialogTitle>
          <DialogDescription>
            This action will mark the report as archived. Archived reports are immutable and cannot be modified.
            This action will also increment the report version.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="destructive" onClick={handleArchive} disabled={isPending}>
            {isPending ? "Archiving..." : "Archive"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
