import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { useEffect, useState } from "react";

export function AuthGuard() {
  const { isAuthenticated, isHydrated, checkAuthStatus } = useAuth();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    // Quick sync check on mount if Zustand hasn't hydrated yet
    checkAuthStatus();
    setChecking(false);
  }, [checkAuthStatus]);

  if (!isHydrated || checking) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground animate-pulse">Loading session...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
