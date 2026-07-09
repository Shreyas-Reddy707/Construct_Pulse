import { useQuery } from "@tanstack/react-query";
import { workerApi } from "../api/workerApi";
import { useSearchParams } from "react-router-dom";

export const workerKeys = {
  all: ["workers"] as const,
  lists: () => [...workerKeys.all, "list"] as const,
  list: (params: Record<string, string | null>) => [...workerKeys.lists(), params] as const,
  details: () => [...workerKeys.all, "detail"] as const,
  detail: (id: string) => [...workerKeys.details(), id] as const,
};

export function useWorkers() {
  const [searchParams] = useSearchParams();
  
  // Convert URLSearchParams to a plain object for the query key
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  // Ensure default pagination exists for query key stability
  params.page = params.page || "1";
  params.limit = params.limit || "20";

  return useQuery({
    queryKey: workerKeys.list(params),
    queryFn: () => workerApi.getWorkers(params),
    staleTime: 30 * 1000, // 30 seconds
  });
}
