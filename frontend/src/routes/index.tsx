import { createBrowserRouter } from "react-router-dom";
import { lazy, Suspense } from "react";
import { Skeleton } from "@/components/ui/skeleton";
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

const SiteWorkspaceLayout = lazy(() => import("@/modules/sites/pages/workspace/SiteWorkspaceLayout").then(m => ({ default: m.SiteWorkspaceLayout })));
const SiteRosterTab = lazy(() => import("@/modules/sites/pages/workspace/SiteRosterTab"));
const SiteAttendanceTab = lazy(() => import("@/modules/sites/pages/workspace/SiteAttendanceTab"));
const SiteContractorsTab = lazy(() => import("@/modules/sites/pages/workspace/SiteContractorsTab"));
const SiteMusterTab = lazy(() => import("@/modules/sites/pages/workspace/SiteMusterTab"));

function TabSuspense({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<div className="p-6 space-y-4"><Skeleton className="h-10 w-full" /><Skeleton className="h-64 w-full" /></div>}>
      {children}
    </Suspense>
  );
}

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
            children: [
              {
                index: true,
                element: <SiteDirectoryPage />,
              },
              {
                path: ":id",
                element: (
                  <Suspense fallback={<div className="h-screen w-full flex items-center justify-center"><Skeleton className="h-32 w-full max-w-4xl" /></div>}>
                    <SiteWorkspaceLayout />
                  </Suspense>
                ),
                children: [
                  {
                    index: true,
                    element: <TabSuspense><SiteRosterTab /></TabSuspense>,
                  },
                  {
                    path: "attendance",
                    element: <TabSuspense><SiteAttendanceTab /></TabSuspense>,
                  },
                  {
                    path: "contractors",
                    element: <TabSuspense><SiteContractorsTab /></TabSuspense>,
                  },
                  {
                    path: "muster",
                    element: <TabSuspense><SiteMusterTab /></TabSuspense>,
                  },
                ],
              },
            ],
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
