import { apiClient } from "@/api/client";
import type { Contractor, ContractorDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";
import type { 
  BackendPaginatedResponse
} from "@/api/adapters/pagination";
import { mapPagination } from "@/api/adapters/pagination";
import type { 
  BackendContractorResponse
} from "@/api/adapters/contractor";
import {
  mapContractor, 
  mapContractorDetail 
} from "@/api/adapters/contractor";

export const contractorApi = {
  getContractors: async (params: Record<string, string | null>): Promise<PaginatedResponse<Contractor>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<BackendPaginatedResponse<BackendContractorResponse>>(`/contractors?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapContractor);
  },

  getContractorById: async (id: string): Promise<ContractorDetail> => {
    const response = await apiClient.get<BackendContractorResponse>(`/contractors/${id}/workspace`);
    
    return mapContractorDetail(response.data);
  },
};
