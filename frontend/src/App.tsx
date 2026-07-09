import { RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { ErrorBoundary } from "@/providers/ErrorBoundary";
import { queryClient } from "@/lib/queryClient";
import { router } from "@/routes";
import { Toaster } from "@/components/ui/sonner";
import { useEffect } from "react";
import { useAuthStore } from "@/store/useAuthStore";

export default function App() {
  const setHydrated = useAuthStore((state) => state.setHydrated);

  useEffect(() => {
    // In a real app with persistent storage (like localStorage zustand middleware),
    // hydration logic goes here. For MVP in-memory + simple token, we can just mark as hydrated.
    setHydrated(true);
  }, [setHydrated]);

  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="system" storageKey="construct-pulse-theme">
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
          <Toaster />
        </QueryClientProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
