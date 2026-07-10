import { ShieldAlert, ShieldCheck } from "lucide-react";

export default function ContractorComplianceTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg flex items-center gap-2">
          <ShieldCheck className="h-5 w-5 text-primary" />
          Compliance Documents
        </h3>
        <p className="text-sm text-muted-foreground">
          Manage business licenses, insurance certificates, and safety plans.
        </p>
      </div>

      <div className="bg-card border rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
          <ShieldAlert className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg">Compliance Tracking</h4>
          <p className="text-sm text-muted-foreground mt-2">
            The full compliance document tracking system is scheduled for a future release. 
            This module will support PDF uploads, expiration date tracking, and automated suspension for expired general liability insurance.
          </p>
        </div>
      </div>
    </div>
  );
}
