import { useOutletContext, Link } from "react-router-dom";
import type { WorkerDetail } from "../../types";
import { Building2, ArrowRight } from "lucide-react";

export function WorkerSiteAccessTab() {
  const { worker } = useOutletContext<{ worker?: WorkerDetail }>();

  if (!worker) return null;

  // For MVP, we assume they are authorized for the site they are currently checked into
  // or a placeholder if none. In a real system this would hit `GET /workers/:id/sites`.
  const activeSite = worker.current_site;

  return (
    <div className="space-y-6">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Authorized Sites</h3>
        <p className="text-sm text-muted-foreground">
          Sites this worker has completed inductions for and is authorized to enter.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {activeSite ? (
          <div className="bg-card text-card-foreground shadow-sm border rounded-xl p-4 flex items-center justify-between group hover:border-primary transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <p className="font-medium">{activeSite}</p>
                <p className="text-sm text-muted-foreground">Currently Assigned</p>
              </div>
            </div>
            {/* Real link would go to /sites/:id */}
            <Link to={`/sites/temp-site-id`} className="p-2 text-muted-foreground group-hover:text-primary transition-colors">
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        ) : (
          <div className="col-span-full py-8 text-center bg-muted/20 border border-dashed rounded-xl">
            <p className="text-muted-foreground">No site authorizations found.</p>
          </div>
        )}
      </div>
    </div>
  );
}
