import type { ScanMode, AttendanceScanPayload, AttendanceScanResponse } from "../types";

class ScannerService {
  private scanDebounceCache: Map<string, number> = new Map();
  private DEBOUNCE_MS = 3000;

  public async processScan(
    qrData: string,
    siteId: string,
    mode: ScanMode,
    submitMutation: (payload: AttendanceScanPayload) => Promise<AttendanceScanResponse>
  ): Promise<AttendanceScanResponse> {
    const now = Date.now();
    const lastScan = this.scanDebounceCache.get(qrData);

    if (lastScan && now - lastScan < this.DEBOUNCE_MS) {
      // Ignore debounced duplicate scans on the client side silently
      return {
        status: "SUCCESS",
        message: "Scan debounced client-side.",
      };
    }

    // Register this scan in the debounce cache
    this.scanDebounceCache.set(qrData, now);

    try {
      // We pass the actual API invocation from the React component (which holds React Query context)
      const payload: AttendanceScanPayload = {
        worker_id: qrData,
        site_id: siteId,
        scan_type: mode,
        timestamp: new Date().toISOString(),
      };

      const result = await submitMutation(payload);
      return result;
    } catch (error) {
      return {
        status: "UNKNOWN_ERROR",
        message: "An unexpected error occurred during scanning.",
      };
    }
  }

  public clearDebounceCache() {
    this.scanDebounceCache.clear();
  }
}

export const scannerService = new ScannerService();
