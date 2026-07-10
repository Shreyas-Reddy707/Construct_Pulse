import type { ScanMode } from "../types";

interface ModeToggleProps {
  mode: ScanMode;
  onModeChange: (mode: ScanMode) => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="flex w-full bg-muted p-1 rounded-xl gap-1">
      <button
        type="button"
        onClick={() => onModeChange("check_in")}
        className={`flex-1 text-lg font-bold py-4 rounded-lg transition-colors ${
          mode === "check_in" 
            ? "bg-primary text-primary-foreground shadow-sm" 
            : "text-muted-foreground hover:bg-background/50"
        }`}
      >
        CHECK IN
      </button>
      <button
        type="button"
        onClick={() => onModeChange("check_out")}
        className={`flex-1 text-lg font-bold py-4 rounded-lg transition-colors ${
          mode === "check_out" 
            ? "bg-secondary text-secondary-foreground shadow-sm" 
            : "text-muted-foreground hover:bg-background/50"
        }`}
      >
        CHECK OUT
      </button>
    </div>
  );
}
