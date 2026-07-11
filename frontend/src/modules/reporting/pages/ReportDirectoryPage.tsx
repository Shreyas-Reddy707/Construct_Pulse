import { useMemo } from "react";
import { Link } from "react-router-dom";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/DataTable";
import { useReports, useReportingDashboard } from "../hooks/useReports";
import type { ComplianceReport } from "../types";
import { ReportStatusBadge } from "../components/ReportStatusBadge";
import { GenerateReportDialog } from "../components/GenerateReportDialog";
import { ArchiveReportDialog } from "../components/ArchiveReportDialog";
import { Button } from "@/components/ui/button";
import { Plus, Archive, FileText, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function ReportDirectoryPage() {
  const { data: reports = [], isLoading: isLoadingReports, isError, refetch } = useReports();
  const { data: dashboard, isLoading: isLoadingDashboard } = useReportingDashboard();

  const columns = useMemo<ColumnDef<ComplianceReport>[]>(
    () => [
      {
        accessorKey: "reportNumber",
        header: "Report Number",
        cell: ({ row }) => (
          <Link to={`/reports/${row.original.id}`} className="font-medium text-primary hover:underline">
            {row.getValue("reportNumber")}
          </Link>
        ),
      },
      {
        accessorKey: "reportType",
        header: "Type",
        cell: ({ row }) => {
          const type = row.getValue("reportType") as string;
          return type.replace(/_/g, " ");
        },
      },
      {
        accessorKey: "reportStatus",
        header: "Status",
        cell: ({ row }) => <ReportStatusBadge status={row.original.reportStatus} />,
      },
      {
        accessorKey: "generatedAt",
        header: "Generated At",
        cell: ({ row }) => {
          const date = row.getValue("generatedAt") as string;
          return new Date(date).toLocaleString();
        },
      },
      {
        id: "actions",
        cell: ({ row }) => {
          const report = row.original;
          return (
            <div className="flex justify-end gap-2">
              <Link to={`/reports/${report.id}`}>
                <Button variant="ghost" size="sm">
                  <ArrowRight className="h-4 w-4 mr-2" />
                  View
                </Button>
              </Link>
              {report.reportStatus !== "ARCHIVED" && (
                <ArchiveReportDialog reportId={report.id}>
                  <Button variant="outline" size="sm" className="text-destructive hover:text-destructive">
                    <Archive className="h-4 w-4 mr-2" />
                    Archive
                  </Button>
                </ArchiveReportDialog>
              )}
            </div>
          );
        },
      },
    ],
    []
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reporting & Analytics</h1>
          <p className="text-muted-foreground mt-2">
            Generate and manage compliance snapshots and analytics.
          </p>
        </div>
        <GenerateReportDialog>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Generate Report
          </Button>
        </GenerateReportDialog>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Generated Reports</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoadingDashboard ? "-" : dashboard?.summary.generated ?? 0}
            </div>
            <p className="text-xs text-muted-foreground">Active compliance snapshots</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Archived Reports</CardTitle>
            <Archive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoadingDashboard ? "-" : dashboard?.summary.archived ?? 0}
            </div>
            <p className="text-xs text-muted-foreground">Immutable historical records</p>
          </CardContent>
        </Card>
      </div>

      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <DataTable
          columns={columns}
          data={reports}
          pageCount={1}
          totalRows={reports.length}
          isLoading={isLoadingReports}
          isError={isError}
          onRetry={refetch}
          config={{
            enableRowSelection: false,
            enableColumnVisibility: false,
            mobileBehavior: "scroll",
            searchableFields: [],
            filterableColumns: [
              {
                id: "reportStatus",
                title: "Status",
                options: [
                  { label: "Generated", value: "GENERATED" },
                  { label: "Archived", value: "ARCHIVED" },
                ],
              },
            ],
          }}
        />
      </div>
    </div>
  );
}
