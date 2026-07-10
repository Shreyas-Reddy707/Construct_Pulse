import { useQuery } from "@tanstack/react-query";
import { departmentApi } from "../api/departmentApi";
import { useSearchParams } from "react-router-dom";

export const departmentKeys = {
  all: ["departments"] as const,
  lists: () => [...departmentKeys.all, "list"] as const,
  list: (params: Record<string, string | null>) => [...departmentKeys.lists(), params] as const,
  details: () => [...departmentKeys.all, "detail"] as const,
  detail: (id: string) => [...departmentKeys.details(), id] as const,
};

export function useDepartments() {
  const [searchParams] = useSearchParams();

  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "20";

  return useQuery({
    queryKey: departmentKeys.list(params),
    queryFn: () => departmentApi.getDepartments(params),
    staleTime: 30 * 1000,
  });
}
