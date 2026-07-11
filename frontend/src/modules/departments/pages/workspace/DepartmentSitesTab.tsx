import { Building2, Info } from "lucide-react";

export default function DepartmentSitesTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg flex items-center gap-2">
          <Building2 className="h-5 w-5 text-primary" />
          Deployed Sites
        </h3>
        <p className="text-sm text-muted-foreground">
          Geographic locations where this department's resources are currently deployed.
        </p>
      </div>

      <div className="bg-card border rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
          <Info className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg">Department Site Tracking</h4>
          <p className="text-sm text-muted-foreground mt-2">
            The active sites view is intentionally deferred. Department-scoped site visibility will be available 
            in a future API unfreeze sprint when the backend is extended to support efficient department filtering.
          </p>
        </div>
      </div>
    </div>
  );
}
