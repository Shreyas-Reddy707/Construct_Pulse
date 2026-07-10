import { useMutation, useQueryClient } from "@tanstack/react-query";
import { attendanceApi } from "../api/attendanceApi";
import type { AttendanceScanPayload, AttendanceScanResponse } from "../types";

export function useAttendanceScan() {
  const queryClient = useQueryClient();

  return useMutation<AttendanceScanResponse, Error, AttendanceScanPayload>({
    mutationFn: (payload) => attendanceApi.submitScan(payload),
    onSuccess: () => {
      // Invalidate relevant queries but keep it targeted to lists
      // so occupancy counts and worker statuses refresh on dashboards.
      queryClient.invalidateQueries({ queryKey: ["workers", "list"] });
      queryClient.invalidateQueries({ queryKey: ["sites", "list"] });
    },
  });
}
