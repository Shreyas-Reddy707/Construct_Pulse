import { Outlet, useParams, useLocation, Link } from "react-router-dom";
import { useDepartment } from "../../hooks/useDepartment";
import { DepartmentWorkspaceHeader } from "../../components/workspace/DepartmentWorkspaceHeader";

export function DepartmentWorkspaceLayout() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const { data: department, isLoading } = useDepartment(id!);

  // Navigation tabs definition
  const tabs = [
    { name: "Department Roster", path: `/departments/${id}` },
    { name: "Deployed Sites", path: `/departments/${id}/sites` },
    { name: "Attendance Log", path: `/departments/${id}/attendance` },
    { name: "Crew Planning", path: `/departments/${id}/planning` },
    { name: "Documentation", path: `/departments/${id}/documents` },
  ];

  const currentPath = location.pathname;

  return (
    <div className="flex flex-col min-h-screen bg-background -mx-6 -mt-6">
      <DepartmentWorkspaceHeader department={department} isLoading={isLoading} />
      
      <div className="flex-1 w-full flex flex-col min-w-0">
        <div className="sticky top-[73px] sm:top-[113px] z-10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b">
          <div className="px-6">
            <nav className="flex space-x-6 overflow-x-auto scrollbar-hide">
              {tabs.map((tab) => {
                const isActive = tab.name === "Department Roster" 
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
          <Outlet context={{ department, isLoading }} />
        </div>
      </div>
    </div>
  );
}
