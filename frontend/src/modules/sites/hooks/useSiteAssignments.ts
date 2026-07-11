import { useQuery } from "@tanstack/react-query";
import { siteApi } from "../api/siteApi";
import { siteKeys } from "./useSites";

export const siteAssignmentKeys = {
  all: (siteId: string) => [...siteKeys.detail(siteId), "assignments"] as const,
};

export function useSiteAssignments(siteId: string | undefined) {
  return useQuery({
    queryKey: siteId ? siteAssignmentKeys.all(siteId) : [],
    queryFn: () => siteApi.getSiteAssignments(siteId!),
    enabled: !!siteId,
    staleTime: 2 * 60 * 1000,
  });
}
