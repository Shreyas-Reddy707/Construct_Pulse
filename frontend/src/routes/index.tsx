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
import { ReportDirectoryPage } from "@/modules/reporting/pages/ReportDirectoryPage";
import { ReportDetailPage } from "@/modules/reporting/pages/ReportDetailPage";
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

const ContractorWorkspaceLayout = lazy(() => import("@/modules/contractors/pages/workspace/ContractorWorkspaceLayout").then(m => ({ default: m.ContractorWorkspaceLayout })));
const ContractorRosterTab = lazy(() => import("@/modules/contractors/pages/workspace/ContractorRosterTab"));
const ContractorSitesTab = lazy(() => import("@/modules/contractors/pages/workspace/ContractorSitesTab"));
const ContractorAttendanceTab = lazy(() => import("@/modules/contractors/pages/workspace/ContractorAttendanceTab"));
const ContractorComplianceTab = lazy(() => import("@/modules/contractors/pages/workspace/ContractorComplianceTab"));
const ContractorPayrollTab = lazy(() => import("@/modules/contractors/pages/workspace/ContractorPayrollTab"));

const DepartmentWorkspaceLayout = lazy(() => import("@/modules/departments/pages/workspace/DepartmentWorkspaceLayout").then(m => ({ default: m.DepartmentWorkspaceLayout })));
const DepartmentRosterTab = lazy(() => import("@/modules/departments/pages/workspace/DepartmentRosterTab"));
const DepartmentSitesTab = lazy(() => import("@/modules/departments/pages/workspace/DepartmentSitesTab"));
const DepartmentAttendanceTab = lazy(() => import("@/modules/departments/pages/workspace/DepartmentAttendanceTab"));
const DepartmentPlanningTab = lazy(() => import("@/modules/departments/pages/workspace/DepartmentPlanningTab"));
const DepartmentDocumentsTab = lazy(() => import("@/modules/departments/pages/workspace/DepartmentDocumentsTab"));

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
            children: [
              {
                index: true,
                element: <DepartmentDirectoryPage />,
              },
              {
                path: ":id",
                element: (
                  <Suspense fallback={<div className="h-screen w-full flex items-center justify-center"><Skeleton className="h-32 w-full max-w-4xl" /></div>}>
                    <DepartmentWorkspaceLayout />
                  </Suspense>
                ),
                children: [
                  {
                    index: true,
                    element: <TabSuspense><DepartmentRosterTab /></TabSuspense>,
                  },
                  {
                    path: "sites",
                    element: <TabSuspense><DepartmentSitesTab /></TabSuspense>,
                  },
                  {
                    path: "attendance",
                    element: <TabSuspense><DepartmentAttendanceTab /></TabSuspense>,
                  },
                  {
                    path: "planning",
                    element: <TabSuspense><DepartmentPlanningTab /></TabSuspense>,
                  },
                  {
                    path: "documents",
                    element: <TabSuspense><DepartmentDocumentsTab /></TabSuspense>,
                  },
                ],
              },
            ],
          },
          {
            path: "contractors",
            children: [
              {
                index: true,
                element: <ContractorDirectoryPage />,
              },
              {
                path: ":id",
                element: (
                  <Suspense fallback={<div className="h-screen w-full flex items-center justify-center"><Skeleton className="h-32 w-full max-w-4xl" /></div>}>
                    <ContractorWorkspaceLayout />
                  </Suspense>
                ),
                children: [
                  {
                    index: true,
                    element: <TabSuspense><ContractorRosterTab /></TabSuspense>,
                  },
                  {
                    path: "sites",
                    element: <TabSuspense><ContractorSitesTab /></TabSuspense>,
                  },
                  {
                    path: "attendance",
                    element: <TabSuspense><ContractorAttendanceTab /></TabSuspense>,
                  },
                  {
                    path: "compliance",
                    element: <TabSuspense><ContractorComplianceTab /></TabSuspense>,
                  },
                  {
                    path: "payroll",
                    element: <TabSuspense><ContractorPayrollTab /></TabSuspense>,
                  },
                ],
              },
            ],
          },
          {
            path: "visitors",
            element: <VisitorDirectoryPage />,
          },
          {
            path: "kiosk",
            element: <KioskPage />,
          },
          {
            path: "reports",
            children: [
              {
                index: true,
                element: <ReportDirectoryPage />,
              },
              {
                path: ":id",
                element: <ReportDetailPage />,
              },
            ],
          },
          // Future protected routes go here
        ],
      },
    ],
  },
]);
