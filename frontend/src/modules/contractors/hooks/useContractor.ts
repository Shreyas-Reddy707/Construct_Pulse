import { useQuery } from "@tanstack/react-query";
import { contractorApi } from "../api/contractorApi";
import { contractorKeys } from "./useContractors";

export function useContractor(id: string) {
  return useQuery({
    queryKey: contractorKeys.detail(id),
    queryFn: () => contractorApi.getContractorById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
