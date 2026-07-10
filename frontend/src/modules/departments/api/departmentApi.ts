import { apiClient } from "@/api/client";
import type { Department, DepartmentDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";

export const departmentApi = {
  getDepartments: async (params: Record<string, string | null>): Promise<PaginatedResponse<Department>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<PaginatedResponse<Department>>(`/departments?${searchParams.toString()}`);
    return response.data;
  },

  getDepartmentById: async (id: string): Promise<DepartmentDetail> => {
    const response = await apiClient.get<DepartmentDetail>(`/departments/${id}`);
    return response.data;
  },
};
