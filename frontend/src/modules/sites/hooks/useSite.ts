import { useQuery } from "@tanstack/react-query";
import { siteApi } from "../api/siteApi";
import { siteKeys } from "./useSites";

export function useSite(id: string) {
  return useQuery({
    queryKey: siteKeys.detail(id),
    queryFn: () => siteApi.getSiteById(id),
    enabled: !!id,
    refetchInterval: 30000,
    refetchIntervalInBackground: false,
  });
}
