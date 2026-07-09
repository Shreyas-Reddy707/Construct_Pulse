import { apiClient } from "@/api/client";
import type { Site, PaginatedResponse } from "../types";

export const siteApi = {
  getSites: async (params: Record<string, string | null>): Promise<PaginatedResponse<Site>> => {
    // Convert object to actual URLSearchParams to clean out nulls and format correctly
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });

    const response = await apiClient.get<PaginatedResponse<Site>>(`/sites?${searchParams.toString()}`);
    return response.data;
  },
};
