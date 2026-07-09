import { Outlet } from "react-router-dom";
import { useUIStore } from "@/store/useUIStore";

export function DashboardLayout() {
  const { sidebarOpen } = useUIStore();

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {sidebarOpen && (
        <aside className="w-64 border-r bg-card p-4 shadow-sm">
          <p className="font-semibold">Sidebar (Placeholder)</p>
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
