import { apiClient } from "@/api/client";
import type { Department, PaginatedResponse } from "../types";

export const departmentApi = {
  getDepartments: async (params: Record<string, string | null>): Promise<PaginatedResponse<Department>> => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        searchParams.append(key, value);
      }
    });

    const response = await apiClient.get<PaginatedResponse<Department>>(`/departments?${searchParams.toString()}`);
    return response.data;
  },
};
