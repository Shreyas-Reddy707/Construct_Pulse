import { useQuery } from "@tanstack/react-query";
import { attendanceApi } from "../api/attendanceApi";
import { useSearchParams } from "react-router-dom";

export const attendanceKeys = {
  all: ["attendance"] as const,
  workers: () => [...attendanceKeys.all, "worker"] as const,
  worker: (id: string, params: Record<string, string | null>) => [...attendanceKeys.workers(), id, params] as const,
};

export function useAttendanceHistory(workerId: string) {
  const [searchParams] = useSearchParams();
  
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "10";

  return useQuery({
    queryKey: attendanceKeys.worker(workerId, params),
    queryFn: () => attendanceApi.getWorkerHistory(workerId, params),
    enabled: !!workerId,
    staleTime: 60 * 1000,
  });
}
