import { useEffect, useState } from "react";
import type { ScanResult } from "../types";
import { CheckCircle2, XCircle } from "lucide-react";

interface ScannerOverlayProps {
  children: React.ReactNode;
  lastResult: ScanResult | null;
}

export function ScannerOverlay({ children, lastResult }: ScannerOverlayProps) {
  const [flash, setFlash] = useState<"success" | "error" | null>(null);

  useEffect(() => {
    if (!lastResult) return;

    // We consider SUCCESS and ALREADY_... as green flashes. 
    // All others (invalid, network error, inactive) are red flashes.
    const isSuccess = 
      lastResult.status === "SUCCESS" || 
      lastResult.status === "ALREADY_CHECKED_IN" || 
      lastResult.status === "ALREADY_CHECKED_OUT";

    setFlash(isSuccess ? "success" : "error");
    
    // In a real browser environment, we'd trigger Audio here.
    // e.g. new Audio(isSuccess ? '/ding.mp3' : '/buzzer.mp3').play().catch(() => {})

    const timer = setTimeout(() => {
      setFlash(null);
    }, 1500);

    return () => clearTimeout(timer);
  }, [lastResult]);

  return (
    <div className="relative w-full h-full">
      {children}

      {flash && (
        <div 
          className={`absolute inset-0 z-50 flex flex-col items-center justify-center animate-in fade-in duration-200 ${
            flash === "success" ? "bg-green-500/80" : "bg-red-500/80"
          }`}
        >
          {flash === "success" ? (
            <CheckCircle2 className="w-48 h-48 text-white drop-shadow-xl" />
          ) : (
            <XCircle className="w-48 h-48 text-white drop-shadow-xl" />
          )}
          <div className="mt-8 bg-black/50 text-white px-8 py-4 rounded-xl backdrop-blur-md text-center max-w-[80%]">
            <h2 className="text-3xl font-bold mb-2">{lastResult?.workerName || "Worker"}</h2>
            <p className="text-xl">{lastResult?.message}</p>
          </div>
        </div>
      )}
    </div>
  );
}
