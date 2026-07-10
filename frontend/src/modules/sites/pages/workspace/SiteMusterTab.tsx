import { AlertTriangle, ShieldAlert } from "lucide-react";

export default function SiteMusterTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg text-destructive flex items-center gap-2">
          <ShieldAlert className="h-5 w-5" />
          Emergency Muster
        </h3>
        <p className="text-sm text-muted-foreground">
          Activate emergency mode to generate an offline-capable checklist of all workers currently on site.
        </p>
      </div>

      <div className="bg-destructive/5 border border-destructive/20 rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center text-destructive">
          <AlertTriangle className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg text-destructive">Emergency Muster Mode</h4>
          <p className="text-sm text-muted-foreground mt-2">
            This high-priority safety workflow is scheduled for the upcoming HSE sprint. 
            When activated, it will override standard site navigation to provide immediate accountability.
          </p>
        </div>
      </div>
    </div>
  );
}
