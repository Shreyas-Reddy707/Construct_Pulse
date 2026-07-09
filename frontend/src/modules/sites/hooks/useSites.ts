import { useQuery } from "@tanstack/react-query";
import { siteApi } from "../api/siteApi";
import { useSearchParams } from "react-router-dom";

export const siteKeys = {
  all: ["sites"] as const,
  lists: () => [...siteKeys.all, "list"] as const,
  list: (params: Record<string, string | null>) => [...siteKeys.lists(), params] as const,
  details: () => [...siteKeys.all, "detail"] as const,
  detail: (id: string) => [...siteKeys.details(), id] as const,
};

export function useSites() {
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
    queryKey: siteKeys.list(params),
    queryFn: () => siteApi.getSites(params),
    staleTime: 30 * 1000, // 30 seconds
  });
}
