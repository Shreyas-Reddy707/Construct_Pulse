import { apiClient } from "@/api/client";
import type { AttendanceScanPayload, AttendanceScanResponse, AttendanceLog } from "../types";
import type { PaginatedResponse } from "@/modules/workers/types";
import type { 
  BackendAttendancePageResponse
} from "@/api/adapters/pagination";
import { mapAttendancePagination } from "@/api/adapters/pagination";
import type { 
  BackendAttendanceLogResponse,
  BackendAttendanceResponse
} from "@/api/adapters/attendance";
import {
  mapAttendanceLog, 
  mapScanResponse 
} from "@/api/adapters/attendance";

export const attendanceApi = {
  submitScan: async (payload: AttendanceScanPayload): Promise<AttendanceScanResponse> => {
    try {
      const endpoint = payload.scan_type === "check_in" ? "/attendance/check-in" : "/attendance/check-out";
      
      const backendPayload = {
        site_id: payload.site_id,
        qr_token: payload.qr_token,
        gps_latitude: payload.gps_latitude,
        gps_longitude: payload.gps_longitude,
      };

      const response = await apiClient.post<BackendAttendanceResponse>(endpoint, backendPayload);
      
      return mapScanResponse(response.data, payload.scan_type);
    } catch (error: any) {
      if (error.response?.data) {
        // Assume backend returns structured errors
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
    
    const response = await apiClient.get<BackendAttendancePageResponse<BackendAttendanceLogResponse>>(`/attendance/worker/${workerId}?${searchParams.toString()}`);
    return mapAttendancePagination(response.data, mapAttendanceLog);
  },

  getSiteHistory: async (siteId: string, params: Record<string, string | null>): Promise<PaginatedResponse<AttendanceLog>> => {
    const { serializeQueryParams } = await import("@/api/utils");
    const searchParams = serializeQueryParams(params);
    
    const response = await apiClient.get<BackendAttendancePageResponse<BackendAttendanceLogResponse>>(`/attendance/site/${siteId}?${searchParams.toString()}`);
    return mapAttendancePagination(response.data, mapAttendanceLog);
  },

  getContractorHistory: async (contractorId: string, params: Record<string, string | null>): Promise<PaginatedResponse<AttendanceLog>> => {
    const { serializeQueryParams } = await import("@/api/utils");
    const searchParams = serializeQueryParams(params);
    
    const response = await apiClient.get<BackendAttendancePageResponse<BackendAttendanceLogResponse>>(`/attendance/contractor/${contractorId}?${searchParams.toString()}`);
    return mapAttendancePagination(response.data, mapAttendanceLog);
  },

  getDepartmentHistory: async (departmentId: string, params: Record<string, string | null>): Promise<PaginatedResponse<AttendanceLog>> => {
    const { serializeQueryParams } = await import("@/api/utils");
    const searchParams = serializeQueryParams(params);
    
    const response = await apiClient.get<BackendAttendancePageResponse<BackendAttendanceLogResponse>>(`/attendance/department/${departmentId}?${searchParams.toString()}`);
    return mapAttendancePagination(response.data, mapAttendanceLog);
  },
};
