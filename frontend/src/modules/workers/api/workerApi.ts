import { apiClient } from "@/api/client";
import type { Worker, WorkerDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";
import type { 
  BackendPaginatedResponse
} from "@/api/adapters/pagination";
import { mapPagination } from "@/api/adapters/pagination";
import type { 
  BackendUserResponse, 
  BackendWorkerDetailResponse
} from "@/api/adapters/worker";
import {
  mapWorker, 
  mapWorkerDetail 
} from "@/api/adapters/worker";
import { mapSite } from "@/api/adapters/site";
import type { Site } from "@/modules/sites/types";
import type { BackendSiteResponse } from "@/api/adapters/site";

export const workerApi = {
  getWorkers: async (params: Record<string, string | null>): Promise<PaginatedResponse<Worker>> => {
    // Force role filter to "Worker" for the directory
    const queryParams = { ...params, role: "Worker" };
    const searchParams = serializeQueryParams(queryParams);

    const response = await apiClient.get<BackendPaginatedResponse<BackendUserResponse>>(`/users?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapWorker);
  },

  getWorkerById: async (id: string): Promise<WorkerDetail> => {
    const response = await apiClient.get<BackendWorkerDetailResponse>(`/workers/${id}`);
    
    return mapWorkerDetail(response.data);
  },

  getWorkerSites: async (id: string): Promise<Site[]> => {
    const response = await apiClient.get<BackendSiteResponse[]>(`/users/${id}/sites`);
    return response.data.map(mapSite);
  },

  approveWorker: async (id: string): Promise<Worker> => {
    const response = await apiClient.put<BackendUserResponse>(`/users/${id}/approve`);
    return mapWorker(response.data);
  },

  rejectWorker: async (id: string): Promise<Worker> => {
    const response = await apiClient.put<BackendUserResponse>(`/users/${id}/reject`);
    return mapWorker(response.data);
  },

  suspendWorker: async (id: string): Promise<Worker> => {
    const response = await apiClient.put<BackendUserResponse>(`/users/${id}/suspend`);
    return mapWorker(response.data);
  },
};
