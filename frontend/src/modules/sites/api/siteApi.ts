import { apiClient } from "@/api/client";
import type { Site, SiteDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";
import type { 
  BackendPaginatedResponse
} from "@/api/adapters/pagination";
import { mapPagination } from "@/api/adapters/pagination";
import type { 
  BackendSiteResponse
} from "@/api/adapters/site";
import {
  mapSite, 
  mapSiteDetail 
} from "@/api/adapters/site";

export const siteApi = {
  getSites: async (params: Record<string, string | null>): Promise<PaginatedResponse<Site>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<BackendPaginatedResponse<BackendSiteResponse>>(`/sites?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapSite);
  },

  getSiteById: async (id: string): Promise<SiteDetail> => {
    const response = await apiClient.get<BackendSiteResponse>(`/sites/${id}`);
    
    return mapSiteDetail(response.data);
  },
};
