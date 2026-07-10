import { useState, useCallback } from "react";
import { ModeToggle } from "../components/ModeToggle";
import { ScannerCamera } from "../components/ScannerCamera";
import { ScannerOverlay } from "../components/ScannerOverlay";
import { scannerService } from "../services/ScannerService";
import { useAttendanceScan } from "../hooks/useAttendance";
import type { ScanMode, ScanResult } from "../types";

// For MVP, we assume the kiosk is deployed to a specific site. 
// In a full production setup, the foreman would select the site upon opening the app,
// or the site ID would be embedded in the device MDM configuration.
const ACTIVE_SITE_ID = "00000000-0000-0000-0000-000000000000";

export function KioskPage() {
  const [mode, setMode] = useState<ScanMode>("check_in");
  const [lastResult, setLastResult] = useState<ScanResult | null>(null);
  const [isScanning, setIsScanning] = useState(false);

  const { mutateAsync } = useAttendanceScan();

  const handleScan = useCallback(async (qrData: string) => {
    if (isScanning) return; // Prevent concurrent invocations while awaiting a promise
    
    setIsScanning(true);
    
    // Call the Service layer (which isolates hardware/debouncing from the UI)
    const result = await scannerService.processScan(qrData, ACTIVE_SITE_ID, mode, mutateAsync);
    
    setLastResult(result);
    setIsScanning(false);
  }, [mode, mutateAsync, isScanning]);

  const handleModeChange = (newMode: ScanMode) => {
    setMode(newMode);
    setLastResult(null);
    scannerService.clearDebounceCache();
  };

  return (
    <div className="flex flex-col h-screen max-h-screen bg-background p-4 md:p-8 overflow-hidden gap-6 max-w-4xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-4xl md:text-5xl font-black tracking-tight uppercase">
          Site Access Kiosk
        </h1>
        <p className="text-muted-foreground text-lg">
          Please scan your badge to record attendance.
        </p>
      </div>

      <ModeToggle mode={mode} onModeChange={handleModeChange} />

      <div className="flex-1 min-h-0">
        <ScannerOverlay lastResult={lastResult}>
          <ScannerCamera onScan={handleScan} isActive={!isScanning} />
        </ScannerOverlay>
      </div>
      
      <div className="text-center text-sm text-muted-foreground">
        Active Site ID: {ACTIVE_SITE_ID}
      </div>
    </div>
  );
}
