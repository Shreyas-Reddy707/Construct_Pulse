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
import type { Worker } from "@/modules/workers/types";
import type { Contractor } from "@/modules/contractors/types";
import { mapWorker } from "@/api/adapters/worker";
import { mapContractor } from "@/api/adapters/contractor";

export interface SiteAssignments {
  workers: Worker[];
  contractors: Contractor[];
}

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

  getSiteAssignments: async (siteId: string): Promise<SiteAssignments> => {
    const response = await apiClient.get<any>(`/sites/${siteId}/assignments`);
    return {
      workers: response.data.workers ? response.data.workers.map(mapWorker) : [],
      contractors: response.data.contractors ? response.data.contractors.map(mapContractor) : [],
    };
  },

  assignWorker: async (siteId: string, workerId: string): Promise<void> => {
    await apiClient.post(`/sites/${siteId}/assign-worker`, { worker_id: workerId });
  },

  unassignWorker: async (siteId: string, workerId: string): Promise<void> => {
    await apiClient.delete(`/sites/${siteId}/unassign-worker/${workerId}`);
  },

  activateSite: async (siteId: string): Promise<void> => {
    await apiClient.post(`/sites/${siteId}/activate`);
  },

  suspendSite: async (siteId: string, reason: string): Promise<void> => {
    await apiClient.post(`/sites/${siteId}/suspend`, { suspension_reason: reason });
  },
};
