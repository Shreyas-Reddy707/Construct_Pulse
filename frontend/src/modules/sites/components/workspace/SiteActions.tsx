import { useState } from "react";
import type { SiteDetail } from "../../types";
import { useSiteActions } from "../../hooks/useSiteActions";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PlayCircle, PauseCircle, Loader2 } from "lucide-react";

interface SiteActionsProps {
  site: SiteDetail;
}

export function SiteActions({ site }: SiteActionsProps) {
  const { activateMutation, suspendMutation } = useSiteActions();
  const [isSuspendDialogOpen, setIsSuspendDialogOpen] = useState(false);
  const [suspendReason, setSuspendReason] = useState("");

  const isPending = activateMutation.isPending || suspendMutation.isPending;

  const handleActivate = () => {
    activateMutation.mutate(site.id);
  };

  const handleSuspend = () => {
    suspendMutation.mutate(
      { siteId: site.id, reason: suspendReason || "Administrative Suspension" },
      {
        onSettled: () => {
          setIsSuspendDialogOpen(false);
          setSuspendReason("");
        },
      }
    );
  };

  return (
    <>
      <div className="flex flex-wrap gap-2">
        <Button
          variant="default"
          size="sm"
          onClick={handleActivate}
          disabled={isPending || site.status === "active"}
          className="bg-green-600 hover:bg-green-700 text-white"
        >
          {activateMutation.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <PlayCircle className="w-4 h-4 mr-2" />
          )}
          Activate
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsSuspendDialogOpen(true)}
          disabled={isPending || site.status === "paused"}
          className="text-orange-600 hover:text-orange-700 hover:bg-orange-50 border-orange-200"
        >
          {suspendMutation.isPending ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <PauseCircle className="w-4 h-4 mr-2" />
          )}
          Suspend
        </Button>
      </div>

      <Dialog open={isSuspendDialogOpen} onOpenChange={setIsSuspendDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Suspend Site</DialogTitle>
            <DialogDescription>
              Are you sure you want to suspend{" "}
              <span className="font-semibold text-foreground">{site.name}</span>?
              This will pause all operations and prevent workers from checking in.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="reason">Suspension Reason</Label>
              <Input
                id="reason"
                placeholder="e.g. Weather conditions, permit issues..."
                value={suspendReason}
                onChange={(e) => setSuspendReason(e.target.value)}
                disabled={isPending}
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setIsSuspendDialogOpen(false)}
              disabled={isPending}
            >
              Cancel
            </Button>
            <Button
              variant="default"
              className="bg-orange-600 hover:bg-orange-700 text-white"
              onClick={handleSuspend}
              disabled={isPending}
            >
              {isPending && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              Suspend
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
