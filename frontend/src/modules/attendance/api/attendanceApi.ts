import { apiClient } from "@/api/client";
import type { AttendanceScanPayload, AttendanceScanResponse } from "../types";

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
};
