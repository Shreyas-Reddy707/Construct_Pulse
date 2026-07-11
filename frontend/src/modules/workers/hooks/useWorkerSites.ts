import { useQuery } from "@tanstack/react-query";
import { workerApi } from "../api/workerApi";
import { workerKeys } from "./useWorkers";

export const workerSiteKeys = {
  all: (id: string) => [...workerKeys.detail(id), "sites"] as const,
};

export function useWorkerSites(workerId: string | undefined) {
  return useQuery({
    queryKey: workerId ? workerSiteKeys.all(workerId) : [],
    queryFn: () => workerApi.getWorkerSites(workerId!),
    enabled: !!workerId,
    staleTime: 5 * 60 * 1000,
  });
}
