import { useQuery } from "@tanstack/react-query";
import { visitorApi } from "../api/visitorApi";
import { useSearchParams } from "react-router-dom";

export const visitorKeys = {
  all: ["visitors"] as const,
  lists: () => [...visitorKeys.all, "list"] as const,
  list: (params: Record<string, string | null>) => [...visitorKeys.lists(), params] as const,
  details: () => [...visitorKeys.all, "detail"] as const,
  detail: (id: string) => [...visitorKeys.details(), id] as const,
};

export function useVisitors() {
  const [searchParams] = useSearchParams();

  const params: Record<string, string | null> = {};
  searchParams.forEach((value, key) => {
    params[key] = value;
  });

  params.page = params.page || "1";
  params.limit = params.limit || "20";

  return useQuery({
    queryKey: visitorKeys.list(params),
    queryFn: () => visitorApi.getVisitors(params),
    staleTime: 30 * 1000,
  });
}
