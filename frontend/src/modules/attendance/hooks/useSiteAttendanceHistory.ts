import { useQuery } from "@tanstack/react-query";
import { attendanceApi } from "../api/attendanceApi";
import { useSearchParams } from "react-router-dom";
import { attendanceKeys } from "./useAttendanceHistory";

export const siteAttendanceKeys = {
  all: () => [...attendanceKeys.all, "site"] as const,
  site: (id: string, params: Record<string, string | null>) => [...siteAttendanceKeys.all(), id, params] as const,
};

export function useSiteAttendanceHistory(siteId: string) {
  const [searchParams] = useSearchParams();
  
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "10";

  return useQuery({
    queryKey: siteAttendanceKeys.site(siteId, params),
    queryFn: () => attendanceApi.getSiteHistory(siteId, params),
    enabled: !!siteId,
    staleTime: 60 * 1000,
  });
}
