import { apiClient } from "@/api/client";
import type { AttendanceScanPayload, AttendanceScanResponse, AttendanceLog } from "../types";
import type { PaginatedResponse } from "@/modules/workers/types"; // using generic response type

export const attendanceApi = {
  submitScan: async (payload: AttendanceScanPayload): Promise<AttendanceScanResponse> => {
    try {
      const response = await apiClient.post<AttendanceScanResponse>("/attendance/scan", payload);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        // Assume backend returns structured errors matching our DTO
        return error.response.data as AttendanceScanResponse;
      }
      return {
        status: "NETWORK_ERROR",
        message: "Failed to connect to the server.",
      };
    }
  },

  getWorkerHistory: async (workerId: string, params: Record<string, string | null>): Promise<PaginatedResponse<AttendanceLog>> => {
    const { serializeQueryParams } = await import("@/api/utils");
    const searchParams = serializeQueryParams(params);
    const response = await apiClient.get<PaginatedResponse<AttendanceLog>>(`/attendance/worker/${workerId}?${searchParams.toString()}`);
    return response.data;
  },
};
