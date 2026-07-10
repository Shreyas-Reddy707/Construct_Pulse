export type ScanMode = "check_in" | "check_out";

export type ScanResultStatus =
  | "SUCCESS"
  | "ALREADY_CHECKED_IN"
  | "ALREADY_CHECKED_OUT"
  | "NOT_ASSIGNED_TO_SITE"
  | "WORKER_INACTIVE"
  | "CONTRACTOR_INACTIVE"
  | "QR_INVALID"
  | "NETWORK_ERROR"
  | "SERVER_ERROR"
  | "UNKNOWN_ERROR";

export interface ScanResult {
  status: ScanResultStatus;
  message: string;
  workerName?: string;
}

export interface AttendanceScanPayload {
  worker_id: string;
  site_id: string;
  scan_type: ScanMode;
  timestamp: string;
}

export interface AttendanceScanResponse {
  status: ScanResultStatus;
  message: string;
  worker_name?: string;
}

export interface AttendanceLog {
  id: string;
  worker_id: string;
  site_id: string;
  site_name: string;
  scan_type: ScanMode;
  timestamp: string;
}
