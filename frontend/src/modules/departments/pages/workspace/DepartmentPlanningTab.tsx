import { CalendarClock, CalendarDays } from "lucide-react";

export default function DepartmentPlanningTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg flex items-center gap-2">
          <CalendarDays className="h-5 w-5 text-primary" />
          Crew Planning & Allocation
        </h3>
        <p className="text-sm text-muted-foreground">
          Forecasting, crew balancing, and future resource scheduling.
        </p>
      </div>

      <div className="bg-card border rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
          <CalendarClock className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg">Workforce Allocation Matrix</h4>
          <p className="text-sm text-muted-foreground mt-2">
            The advanced crew planning module is scheduled for a future enterprise release. 
            This interface will allow department heads to drag-and-drop manpower allocations, balance crew distribution across active sites, and accurately forecast upcoming shift requirements.
          </p>
        </div>
      </div>
    </div>
  );
}
