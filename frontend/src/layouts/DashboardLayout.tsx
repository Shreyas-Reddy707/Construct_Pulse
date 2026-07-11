import { Outlet, Link } from "react-router-dom";
import { useUIStore } from "@/store/useUIStore";

export function DashboardLayout() {
  const { sidebarOpen } = useUIStore();

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
            ].map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className="px-2 py-1.5 rounded-md hover:bg-accent hover:text-accent-foreground text-sm font-medium transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
      )}
      <div className="flex flex-1 flex-col">
        <header className="flex h-14 items-center border-b px-4">
          <p className="font-semibold">Header (Placeholder)</p>
        </header>
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
