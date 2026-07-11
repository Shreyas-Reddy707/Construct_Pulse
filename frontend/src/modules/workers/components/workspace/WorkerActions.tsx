import { useState } from "react";
import type { WorkerDetail } from "../../types";
import { useWorkerActions } from "../../hooks/useWorkerActions";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { CheckCircle2, Ban, XCircle, Loader2 } from "lucide-react";

interface WorkerActionsProps {
  worker: WorkerDetail;
}

type ActionType = "suspend" | "reject" | null;

export function WorkerActions({ worker }: WorkerActionsProps) {
  const { approveMutation, rejectMutation, suspendMutation } = useWorkerActions();
  const [confirmAction, setConfirmAction] = useState<ActionType>(null);

  const isPending =
    approveMutation.isPending ||
    rejectMutation.isPending ||
    suspendMutation.isPending;

  const handleApprove = () => {
    approveMutation.mutate(worker.id);
  };

  const handleConfirmAction = () => {
    if (confirmAction === "suspend") {
      suspendMutation.mutate(worker.id, {
        onSettled: () => setConfirmAction(null),
      });
    } else if (confirmAction === "reject") {
      rejectMutation.mutate(worker.id, {
        onSettled: () => setConfirmAction(null),
      });
    }
  };

  return (
    <>
      <div className="flex flex-wrap gap-2">
        <Button
          variant="default"
          size="sm"
          onClick={handleApprove}
          disabled={isPending || worker.status === "approved"}
          className="bg-green-600 hover:bg-green-700 text-white"
        >
          {approveMutation.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <CheckCircle2 className="w-4 h-4 mr-2" />
          )}
          Approve
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setConfirmAction("reject")}
          disabled={isPending || worker.status === "rejected"}
          className="text-destructive hover:bg-destructive/10"
        >
          {rejectMutation.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <XCircle className="w-4 h-4 mr-2" />
          )}
          Reject
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setConfirmAction("suspend")}
          disabled={isPending || worker.status === "suspended"}
          className="text-orange-600 hover:text-orange-700 hover:bg-orange-50 border-orange-200"
        >
          {suspendMutation.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <Ban className="w-4 h-4 mr-2" />
          )}
          Suspend
        </Button>
      </div>

      <Dialog
        open={confirmAction !== null}
        onOpenChange={(open) => {
          if (!open) setConfirmAction(null);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {confirmAction === "suspend" ? "Suspend Worker?" : "Reject Worker?"}
            </DialogTitle>
            <DialogDescription>
              {confirmAction === "suspend" ? (
                <>
                  Are you sure you want to suspend{" "}
                  <span className="font-semibold text-foreground">
                    {worker.first_name} {worker.last_name}
                  </span>
                  ? This worker will no longer be allowed to check into construction sites.
                </>
              ) : (
                <>
                  Are you sure you want to reject{" "}
                  <span className="font-semibold text-foreground">
                    {worker.first_name} {worker.last_name}
                  </span>
                  ? They will be denied site access permanently unless re-approved.
                </>
              )}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="mt-4">
            <Button
              variant="outline"
              onClick={() => setConfirmAction(null)}
              disabled={isPending}
            >
              Cancel
            </Button>
            <Button
              variant={confirmAction === "suspend" ? "default" : "destructive"}
              className={confirmAction === "suspend" ? "bg-orange-600 hover:bg-orange-700 text-white" : ""}
              onClick={handleConfirmAction}
              disabled={isPending}
            >
              {isPending && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {confirmAction === "suspend" ? "Suspend" : "Reject"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
