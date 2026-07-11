import { Outlet, Link, useLocation } from "react-router-dom";
import { useUIStore } from "@/store/useUIStore";
import { AppHeader } from "@/components/layout/AppHeader";

export function DashboardLayout() {
  const { sidebarOpen } = useUIStore();
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {sidebarOpen && (
        <aside className="w-64 border-r bg-card p-4 shadow-sm flex flex-col gap-2">
          <p className="font-semibold px-2 mb-4">ConstructPulse</p>
          <nav className="flex flex-col gap-1">
            {[
              { path: "/", label: "Dashboard" },
              { path: "/workers", label: "Workers" },
              { path: "/sites", label: "Sites" },
              { path: "/departments", label: "Departments" },
              { path: "/contractors", label: "Contractors" },
              { path: "/visitors", label: "Visitors" },
              { path: "/kiosk", label: "Attendance" },
              { path: "/reports", label: "Reports" },
            ].map((item) => {
              const isActive = item.path === "/" 
                ? currentPath === "/"
                : currentPath.startsWith(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-2 py-1.5 rounded-md text-sm font-medium transition-colors ${
                    isActive 
                      ? "bg-accent text-accent-foreground font-semibold" 
                      : "hover:bg-accent hover:text-accent-foreground text-muted-foreground"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
      )}
      <div className="flex flex-1 flex-col min-w-0">
        <AppHeader />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
