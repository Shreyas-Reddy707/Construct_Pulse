import { useMutation, useQueryClient } from "@tanstack/react-query";
import { siteApi } from "../api/siteApi";
import { siteKeys } from "./useSites";
import { siteAssignmentKeys } from "./useSiteAssignments";
import { toast } from "sonner";

export function useSiteActions() {
  const queryClient = useQueryClient();

  const invalidateSite = (siteId: string) => {
    queryClient.invalidateQueries({ queryKey: siteKeys.detail(siteId) });
    queryClient.invalidateQueries({ queryKey: siteKeys.lists() });
  };

  const invalidateAssignments = (siteId: string) => {
    queryClient.invalidateQueries({ queryKey: siteAssignmentKeys.all(siteId) });
  };

  const activateMutation = useMutation({
    mutationFn: (siteId: string) => siteApi.activateSite(siteId),
    onSuccess: (_, siteId) => {
      toast.success("Site activated successfully");
      invalidateSite(siteId);
    },
    onError: () => {
      toast.error("Failed to activate site");
    },
  });

  const suspendMutation = useMutation({
    mutationFn: ({ siteId, reason }: { siteId: string; reason: string }) =>
      siteApi.suspendSite(siteId, reason),
    onSuccess: (_, { siteId }) => {
      toast.success("Site suspended successfully");
      invalidateSite(siteId);
    },
    onError: () => {
      toast.error("Failed to suspend site");
    },
  });

  const assignWorkerMutation = useMutation({
    mutationFn: ({ siteId, workerId }: { siteId: string; workerId: string }) =>
      siteApi.assignWorker(siteId, workerId),
    onSuccess: (_, { siteId }) => {
      toast.success("Worker assigned successfully");
      invalidateAssignments(siteId);
    },
    onError: () => {
      toast.error("Failed to assign worker");
    },
  });

  const unassignWorkerMutation = useMutation({
    mutationFn: ({ siteId, workerId }: { siteId: string; workerId: string }) =>
      siteApi.unassignWorker(siteId, workerId),
    onSuccess: (_, { siteId }) => {
      toast.success("Worker unassigned successfully");
      invalidateAssignments(siteId);
    },
    onError: () => {
      toast.error("Failed to unassign worker");
    },
  });

  return {
    activateMutation,
    suspendMutation,
    assignWorkerMutation,
    unassignWorkerMutation,
  };
}
