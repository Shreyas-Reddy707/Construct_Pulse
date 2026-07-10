import { useQuery } from "@tanstack/react-query";
import { contractorApi } from "../api/contractorApi";
import { useSearchParams } from "react-router-dom";

export const contractorKeys = {
  all: ["contractors"] as const,
  lists: () => [...contractorKeys.all, "list"] as const,
  list: (params: Record<string, string | null>) => [...contractorKeys.lists(), params] as const,
  details: () => [...contractorKeys.all, "detail"] as const,
  detail: (id: string) => [...contractorKeys.details(), id] as const,
};

export function useContractors() {
  const [searchParams] = useSearchParams();

  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "20";

  return useQuery({
    queryKey: contractorKeys.list(params),
    queryFn: () => contractorApi.getContractors(params),
    staleTime: 30 * 1000,
  });
}
