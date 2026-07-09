import { apiClient } from "@/api/client";
import type { Worker, PaginatedResponse } from "../types";

export const workerApi = {
  getWorkers: async (params: Record<string, string | null>): Promise<PaginatedResponse<Worker>> => {
    // For MVP, if there is no backend wired, we could mock this.
    // However, the prompt says "Map URL search params directly into the existing backend BaseQuery contract."
    // So we'll pass the params directly to axios.
    
    // Convert object to actual URLSearchParams to clean out nulls and format correctly
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });

    const response = await apiClient.get<PaginatedResponse<Worker>>(`/workers?${searchParams.toString()}`);
    return response.data;
  },
};
