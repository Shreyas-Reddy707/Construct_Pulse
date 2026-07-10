import { Banknote, Calculator } from "lucide-react";

export default function ContractorPayrollTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg flex items-center gap-2">
          <Banknote className="h-5 w-5 text-primary" />
          Payroll & Billing
        </h3>
        <p className="text-sm text-muted-foreground">
          Reconcile attendance logs against sub-contractor billing rates.
        </p>
      </div>

      <div className="bg-card border rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
          <Calculator className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg">Payroll Reconciliation</h4>
          <p className="text-sm text-muted-foreground mt-2">
            The payroll and billing module is scheduled for WS7. It will automatically reconcile 
            check-in/check-out logs against negotiated hourly rates to streamline invoice approvals.
          </p>
        </div>
      </div>
    </div>
  );
}
