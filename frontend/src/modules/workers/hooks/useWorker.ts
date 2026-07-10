import { useQuery } from "@tanstack/react-query";
import { workerApi } from "../api/workerApi";

import { workerKeys } from "./useWorkers";

export function useWorker(id: string) {
  return useQuery({
    queryKey: workerKeys.detail(id),
    queryFn: () => workerApi.getWorkerById(id),
    staleTime: 5 * 60 * 1000,
    enabled: !!id,
  });
}
