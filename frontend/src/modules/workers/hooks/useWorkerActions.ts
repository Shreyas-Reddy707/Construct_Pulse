import { useMutation, useQueryClient } from "@tanstack/react-query";
import { workerApi } from "../api/workerApi";
import { workerKeys } from "./useWorkers";
import { toast } from "sonner";

export function useWorkerActions() {
  const queryClient = useQueryClient();

  const invalidateWorker = (id: string) => {
    queryClient.invalidateQueries({ queryKey: workerKeys.detail(id) });
    queryClient.invalidateQueries({ queryKey: workerKeys.lists() });
  };

  const approveMutation = useMutation({
    mutationFn: (id: string) => workerApi.approveWorker(id),
    onSuccess: (_, id) => {
      toast.success("Worker approved successfully");
      invalidateWorker(id);
    },
    onError: () => {
      toast.error("Failed to approve worker");
    },
  });

  const rejectMutation = useMutation({
    mutationFn: (id: string) => workerApi.rejectWorker(id),
    onSuccess: (_, id) => {
      toast.success("Worker rejected successfully");
      invalidateWorker(id);
    },
    onError: () => {
      toast.error("Failed to reject worker");
    },
  });

  const suspendMutation = useMutation({
    mutationFn: (id: string) => workerApi.suspendWorker(id),
    onSuccess: (_, id) => {
      toast.success("Worker suspended successfully");
      invalidateWorker(id);
    },
    onError: () => {
      toast.error("Failed to suspend worker");
    },
  });

  return {
    approveMutation,
    rejectMutation,
    suspendMutation,
  };
}
