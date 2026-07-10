import { apiClient } from "@/api/client";
import type { Site, SiteDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";

export const siteApi = {
  getSites: async (params: Record<string, string | null>): Promise<PaginatedResponse<Site>> => {
    // Convert object to actual URLSearchParams to clean out nulls and format correctly
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<PaginatedResponse<Site>>(`/sites?${searchParams.toString()}`);
    return response.data;
  },

  getSiteById: async (id: string): Promise<SiteDetail> => {
    const response = await apiClient.get<SiteDetail>(`/sites/${id}`);
    return response.data;
  },
};
