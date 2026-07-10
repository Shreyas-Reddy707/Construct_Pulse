import { useState, useRef, useEffect } from "react";
import { QrCode, Keyboard } from "lucide-react";

interface ScannerCameraProps {
  onScan: (qrData: string) => void;
  isActive: boolean;
}

export function ScannerCamera({ onScan, isActive }: ScannerCameraProps) {
  const [manualInput, setManualInput] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-focus the invisible input for hardware barcode scanners
  useEffect(() => {
    if (isActive && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isActive]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && manualInput.trim()) {
      onScan(manualInput.trim());
      setManualInput(""); // Clear for next scan
    }
  };

  return (
    <div className="relative w-full aspect-square md:aspect-video bg-black rounded-xl overflow-hidden flex items-center justify-center border-4 border-muted">
      {/* 
        MVP Note: html5-qrcode dependency is deferred. 
        This is a mock visual placeholder that supports hardware USB barcode scanners 
        (which act as keyboards and emit 'Enter') or manual typing for testing.
      */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-muted-foreground opacity-50 pointer-events-none">
        <QrCode className="w-32 h-32 mb-4" />
        <p className="text-xl font-medium tracking-widest">CAMERA FEED PLACEHOLDER</p>
      </div>
      
      {/* Focus trap for hardware scanners or manual testing */}
      <div className="absolute bottom-4 left-4 right-4 bg-background/80 backdrop-blur-sm p-4 rounded-lg flex items-center gap-3">
        <Keyboard className="w-5 h-5 text-muted-foreground" />
        <input
          ref={inputRef}
          type="text"
          value={manualInput}
          onChange={(e) => setManualInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Awaiting scan or enter ID manually..."
          className="flex-1 bg-transparent border-none outline-none text-foreground font-mono"
          disabled={!isActive}
          autoFocus
        />
      </div>
    </div>
  );
}
