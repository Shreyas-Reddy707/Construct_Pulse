import { Outlet, useParams, useLocation, Link } from "react-router-dom";
import { useWorker } from "../../hooks/useWorker";
import { WorkerWorkspaceHeader } from "../../components/workspace/WorkerWorkspaceHeader";

export function WorkerWorkspaceLayout() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const { data: worker, isLoading } = useWorker(id!);

  // Navigation tabs definition
  const tabs = [
    { name: "Overview", path: `/workers/${id}` },
    { name: "Attendance", path: `/workers/${id}/attendance` },
    { name: "Authorized Sites", path: `/workers/${id}/sites` },
    { name: "Documents", path: `/workers/${id}/documents` },
  ];

  const currentPath = location.pathname;

  return (
    <div className="flex flex-col min-h-screen bg-background -mx-6 -mt-6">
      <WorkerWorkspaceHeader worker={worker} isLoading={isLoading} />
      
      <div className="flex-1 w-full flex flex-col min-w-0">
        <div className="sticky top-[73px] sm:top-[113px] z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b">
          <div className="px-6">
            <nav className="flex space-x-6 overflow-x-auto scrollbar-hide">
              {tabs.map((tab) => {
                // Exact match for Overview since it's the index, otherwise prefix match
                const isActive = tab.name === "Overview" 
                  ? currentPath === tab.path || currentPath === `${tab.path}/`
                  : currentPath.startsWith(tab.path);

                return (
                  <Link
                    key={tab.name}
                    to={tab.path}
                    className={`whitespace-nowrap py-3 border-b-2 font-medium text-sm transition-colors ${
                      isActive
                        ? "border-primary text-primary"
                        : "border-transparent text-muted-foreground hover:text-foreground hover:border-muted"
                    }`}
                  >
                    {tab.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>

        <div className="p-6">
          <Outlet context={{ worker, isLoading }} />
        </div>
      </div>
    </div>
  );
}
