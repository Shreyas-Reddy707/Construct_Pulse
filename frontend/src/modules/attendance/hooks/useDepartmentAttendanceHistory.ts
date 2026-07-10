import { useQuery } from "@tanstack/react-query";
import { attendanceApi } from "../api/attendanceApi";
import { useSearchParams } from "react-router-dom";
import { attendanceKeys } from "./useAttendanceHistory";

export const departmentAttendanceKeys = {
  all: () => [...attendanceKeys.all, "department"] as const,
  department: (id: string, params: Record<string, string | null>) => [...departmentAttendanceKeys.all(), id, params] as const,
};

export function useDepartmentAttendanceHistory(departmentId: string) {
  const [searchParams] = useSearchParams();
  
  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "10";

  return useQuery({
    queryKey: departmentAttendanceKeys.department(departmentId, params),
    queryFn: () => attendanceApi.getDepartmentHistory(departmentId, params),
    enabled: !!departmentId,
    staleTime: 60 * 1000,
  });
}
