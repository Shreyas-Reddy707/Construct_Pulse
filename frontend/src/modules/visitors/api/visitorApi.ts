import { apiClient } from "@/api/client";
import { serializeQueryParams } from "@/api/utils";
import type { Visitor, PaginatedResponse } from "../types";
import type { 
  BackendPaginatedResponse
} from "@/api/adapters/pagination";
import { mapPagination } from "@/api/adapters/pagination";
import type { 
  BackendVisitorResponse
} from "@/api/adapters/visitor";
import { mapVisitor } from "@/api/adapters/visitor";

export const visitorApi = {
  getVisitors: async (params: Record<string, string | null>): Promise<PaginatedResponse<Visitor>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<BackendPaginatedResponse<BackendVisitorResponse>>(`/visitors?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapVisitor);
  },
};
