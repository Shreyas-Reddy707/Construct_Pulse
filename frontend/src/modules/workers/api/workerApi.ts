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

export const workerApi = {
  getWorkers: async (params: Record<string, string | null>): Promise<PaginatedResponse<Worker>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<BackendPaginatedResponse<BackendUserResponse>>(`/workers?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapWorker);
  },

  getWorkerById: async (id: string): Promise<WorkerDetail> => {
    const response = await apiClient.get<BackendWorkerDetailResponse>(`/workers/${id}`);
    
    return mapWorkerDetail(response.data);
  },
};
