import { Outlet, useParams, Link, useLocation } from "react-router-dom";
import { useWorker } from "../../hooks/useWorker";
import { WorkerSidebar } from "../../components/workspace/WorkerSidebar";
import { ChevronRight, ArrowLeft } from "lucide-react";

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
    <div className="space-y-6 pb-10">
      {/* Breadcrumb / Top Bar */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link to="/workers" className="hover:text-foreground flex items-center transition-colors">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Workers
        </Link>
        <ChevronRight className="h-4 w-4" />
        <span className="text-foreground font-medium">Worker Workspace</span>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        {/* Sidebar for Identity and Status */}
        <WorkerSidebar worker={worker} isLoading={isLoading} />

        {/* Main Workspace Content Area */}
        <div className="flex-1 w-full flex flex-col min-w-0">
          {/* Scrollable Tabs for Mobile Support */}
          <div className="overflow-x-auto pb-4 border-b scrollbar-hide">
            <nav className="flex space-x-6 min-w-max px-1">
              {tabs.map((tab) => {
                // Exact match for Overview since it's the index, otherwise prefix match
                const isActive = tab.name === "Overview" 
                  ? currentPath === tab.path || currentPath === `${tab.path}/`
                  : currentPath.startsWith(tab.path);

                return (
                  <Link
                    key={tab.name}
                    to={tab.path}
                    className={`whitespace-nowrap py-2 border-b-2 font-medium text-sm transition-colors ${
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

          {/* Tab Content Router Outlet */}
          <div className="mt-6">
            <Outlet context={{ worker, isLoading }} />
          </div>
        </div>
      </div>
    </div>
  );
}
