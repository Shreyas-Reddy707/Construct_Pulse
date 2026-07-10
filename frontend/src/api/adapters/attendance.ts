import type { AttendanceLog, AttendanceScanResponse, ScanMode } from "@/modules/attendance/types";

export interface BackendAttendanceLogResponse {
  id: string;
  attendance_id: string;
  worker_id: string;
  site_id: string;
  site_name: string;
  scan_type: string;
  timestamp: string;
}

export interface BackendAttendanceResponse {
  id: string;
  user_id: string;
  site_id: string;
  status: string;
  check_in_time?: string | null;
  check_out_time?: string | null;
  method: string;
}

export function mapAttendanceLog(backendLog: BackendAttendanceLogResponse): AttendanceLog {
  return {
    id: backendLog.id,
    worker_id: backendLog.worker_id,
    site_id: backendLog.site_id,
    site_name: backendLog.site_name,
    scan_type: (backendLog.scan_type === "check_in" || backendLog.scan_type === "check_out") 
      ? backendLog.scan_type 
      : "check_in",
    timestamp: backendLog.timestamp,
  };
}

export function mapScanResponse(_backendResponse: BackendAttendanceResponse, scanType: ScanMode): AttendanceScanResponse {
  return {
    status: "SUCCESS", // Note: Error mappings (like ALREADY_CHECKED_IN) should be handled in the API error interceptor
    message: `Successfully ${scanType === "check_in" ? "checked in" : "checked out"}`,
    worker_name: "Worker", // The backend doesn't return the worker's name in the raw attendance response for now
  };
}
