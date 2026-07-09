import { RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { ErrorBoundary } from "@/providers/ErrorBoundary";
import { queryClient } from "@/lib/queryClient";
import { router } from "@/routes";
import { Toaster } from "@/components/ui/sonner";
import { useAppBootstrap } from "@/modules/app/hooks/useAppBootstrap";

export default function App() {
  useAppBootstrap();

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
