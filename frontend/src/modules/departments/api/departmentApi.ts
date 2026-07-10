import { apiClient } from "@/api/client";
import type { Department, DepartmentDetail, PaginatedResponse } from "../types";
import { serializeQueryParams } from "@/api/utils";
import type { 
  BackendPaginatedResponse
} from "@/api/adapters/pagination";
import { mapPagination } from "@/api/adapters/pagination";
import type { 
  BackendDepartmentResponse
} from "@/api/adapters/department";
import {
  mapDepartment, 
  mapDepartmentDetail 
} from "@/api/adapters/department";

export const departmentApi = {
  getDepartments: async (params: Record<string, string | null>): Promise<PaginatedResponse<Department>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<BackendPaginatedResponse<BackendDepartmentResponse>>(`/departments?${searchParams.toString()}`);
    
    return mapPagination(response.data, mapDepartment);
  },

  getDepartmentById: async (id: string): Promise<DepartmentDetail> => {
    const response = await apiClient.get<BackendDepartmentResponse>(`/departments/${id}`);
    
    return mapDepartmentDetail(response.data);
  },
};
