import { createBrowserRouter } from "react-router-dom";
import { AuthLayout } from "@/layouts/AuthLayout";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { AuthGuard } from "./AuthGuard";
import { LoginPage } from "@/modules/auth/pages/LoginPage";
import { DashboardPage } from "@/modules/dashboard/pages/DashboardPage";
import { WorkerDirectoryPage } from "@/modules/workers/pages/WorkerDirectoryPage";
import { SiteDirectoryPage } from "@/modules/sites/pages/SiteDirectoryPage";
import { DepartmentDirectoryPage } from "@/modules/departments/pages/DepartmentDirectoryPage";
import { ContractorDirectoryPage } from "@/modules/contractors/pages/ContractorDirectoryPage";
import { VisitorDirectoryPage } from "@/modules/visitors/pages/VisitorDirectoryPage";
import { KioskPage } from "@/modules/attendance/pages/KioskPage";
import { WorkerWorkspaceLayout } from "@/modules/workers/pages/workspace/WorkerWorkspaceLayout";
import { WorkerOverviewTab } from "@/modules/workers/pages/workspace/WorkerOverviewTab";
import { WorkerAttendanceTab } from "@/modules/workers/pages/workspace/WorkerAttendanceTab";
import { WorkerSiteAccessTab } from "@/modules/workers/pages/workspace/WorkerSiteAccessTab";
import { WorkerDocumentsTab } from "@/modules/workers/pages/workspace/WorkerDocumentsTab";

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
            children: [
              {
                index: true,
                element: <WorkerDirectoryPage />,
              },
              {
                path: ":id",
                element: <WorkerWorkspaceLayout />,
                children: [
                  {
                    index: true,
                    element: <WorkerOverviewTab />,
                  },
                  {
                    path: "attendance",
                    element: <WorkerAttendanceTab />,
                  },
                  {
                    path: "sites",
                    element: <WorkerSiteAccessTab />,
                  },
                  {
                    path: "documents",
                    element: <WorkerDocumentsTab />,
                  },
                ],
              },
            ],
          },
          {
            path: "sites",
            element: <SiteDirectoryPage />,
          },
          {
            path: "departments",
            element: <DepartmentDirectoryPage />,
          },
          {
            path: "contractors",
            element: <ContractorDirectoryPage />,
          },
          {
            path: "visitors",
            element: <VisitorDirectoryPage />,
          },
          {
            path: "kiosk",
            element: <KioskPage />,
          },
          // Future protected routes go here
        ],
      },
    ],
  },
]);
