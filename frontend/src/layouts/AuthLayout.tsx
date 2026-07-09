import { Outlet } from "react-router-dom";

export function AuthLayout() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground">
      <main className="w-full max-w-md p-4">
        <Outlet />
      </main>
    </div>
  );
}
