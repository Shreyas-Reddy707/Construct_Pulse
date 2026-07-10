import { apiClient } from "@/api/client";
import { serializeQueryParams } from "@/api/utils";
import type { Visitor, PaginatedResponse } from "../types";

export const visitorApi = {
  getVisitors: async (params: Record<string, string | null>): Promise<PaginatedResponse<Visitor>> => {
    const searchParams = serializeQueryParams(params);

    const response = await apiClient.get<PaginatedResponse<Visitor>>(`/visitors?${searchParams.toString()}`);
    return response.data;
  },
};
