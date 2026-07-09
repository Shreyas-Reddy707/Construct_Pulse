import { createBrowserRouter } from "react-router-dom";
import { AuthLayout } from "@/layouts/AuthLayout";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { AuthGuard } from "./AuthGuard";
import { LoginPage } from "@/modules/auth/pages/LoginPage";
import { DashboardPage } from "@/modules/dashboard/pages/DashboardPage";
import { WorkerDirectoryPage } from "@/modules/workers/pages/WorkerDirectoryPage";
import { SiteDirectoryPage } from "@/modules/sites/pages/SiteDirectoryPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <AuthLayout />,
    children: [
      {
        index: true,
        element: <LoginPage />,
      },
    ],
  },
  {
    path: "/",
    element: <AuthGuard />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: "workers",
            element: <WorkerDirectoryPage />,
          },
          {
            path: "sites",
            element: <SiteDirectoryPage />,
          },
          // Future protected routes go here
        ],
      },
    ],
  },
]);
