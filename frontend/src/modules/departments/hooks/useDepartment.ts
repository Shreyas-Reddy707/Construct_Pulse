import { useQuery } from "@tanstack/react-query";
import { departmentApi } from "../api/departmentApi";
import { departmentKeys } from "./useDepartments";

export function useDepartment(id: string) {
  return useQuery({
    queryKey: departmentKeys.detail(id),
    queryFn: () => departmentApi.getDepartmentById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
