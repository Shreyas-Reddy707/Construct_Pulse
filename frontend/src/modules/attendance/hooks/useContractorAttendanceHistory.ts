import { useQuery } from "@tanstack/react-query";
import { attendanceApi } from "../api/attendanceApi";
import { useSearchParams } from "react-router-dom";
import { attendanceKeys } from "./useAttendanceHistory";

export const contractorAttendanceKeys = {
  all: () => [...attendanceKeys.all, "contractor"] as const,
  contractor: (id: string, params: Record<string, string | null>) => [...contractorAttendanceKeys.all(), id, params] as const,
};

export function useContractorAttendanceHistory(contractorId: string) {
  const [searchParams] = useSearchParams();
  
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "10";

  return useQuery({
    queryKey: contractorAttendanceKeys.contractor(contractorId, params),
    queryFn: () => attendanceApi.getContractorHistory(contractorId, params),
    enabled: !!contractorId,
    staleTime: 60 * 1000,
  });
}
