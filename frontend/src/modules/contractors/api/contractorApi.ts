import { apiClient } from "@/api/client";
import type { Contractor, PaginatedResponse } from "../types";

export const contractorApi = {
  getContractors: async (params: Record<string, string | null>): Promise<PaginatedResponse<Contractor>> => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });

    const response = await apiClient.get<PaginatedResponse<Contractor>>(`/contractors?${searchParams.toString()}`);
    return response.data;
  },
};
