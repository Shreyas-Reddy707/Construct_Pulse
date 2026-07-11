import { useState } from "react";
import { useWorkers } from "@/modules/workers/hooks/useWorkers";
import { useSiteActions } from "../../hooks/useSiteActions";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2, Plus } from "lucide-react";

interface AssignWorkerDialogProps {
  siteId: string;
}

export function AssignWorkerDialog({ siteId }: AssignWorkerDialogProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedWorkerId, setSelectedWorkerId] = useState<string>("");
  const { data: workersData, isLoading: isLoadingWorkers } = useWorkers();
  const { assignWorkerMutation } = useSiteActions();

  const isPending = assignWorkerMutation.isPending;

  const handleAssign = () => {
    if (!selectedWorkerId) return;

    assignWorkerMutation.mutate(
      { siteId, workerId: selectedWorkerId },
      {
        onSettled: () => {
          setIsOpen(false);
          setSelectedWorkerId("");
        },
      }
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="default" size="sm" className="gap-2">
          <Plus className="w-4 h-4" />
          Assign Worker
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Assign Worker to Site</DialogTitle>
          <DialogDescription>
            Select an existing approved worker to grant them access to this site.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <Select
            value={selectedWorkerId}
            onValueChange={setSelectedWorkerId}
            disabled={isPending || isLoadingWorkers}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select a worker..." />
            </SelectTrigger>
            <SelectContent>
              {workersData?.items
                ?.filter((w) => w.status === "approved") // Only assign approved workers
                .map((worker) => (
                  <SelectItem key={worker.id} value={worker.id}>
                    {worker.first_name} {worker.last_name} ({worker.role})
                  </SelectItem>
                ))}
            </SelectContent>
          </Select>
        </div>
        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => setIsOpen(false)}
            disabled={isPending}
          >
            Cancel
          </Button>
          <Button
            onClick={handleAssign}
            disabled={!selectedWorkerId || isPending}
          >
            {isPending && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
            Assign
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
