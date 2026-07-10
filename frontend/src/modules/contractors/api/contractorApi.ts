import { apiClient } from "@/api/client";
import type { Contractor, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";

export const contractorApi = {
  getContractors: async (params: Record<string, string | null>): Promise<PaginatedResponse<Contractor>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<PaginatedResponse<Contractor>>(`/contractors?${searchParams.toString()}`);
    return response.data;
  },
};
