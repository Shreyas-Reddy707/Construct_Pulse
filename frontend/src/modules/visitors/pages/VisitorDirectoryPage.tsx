import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useVisitors } from "../hooks/useVisitors";
import { visitorColumns } from "../columns/visitorColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const visitorTableConfig: DataTableConfig = {
  enableRowSelection: true,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search visitors or hosts..." },
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Checked In", value: "checked_in" },
        { label: "Scheduled", value: "scheduled" },
        { label: "Checked Out", value: "checked_out" },
        { label: "Denied", value: "denied" },
      ],
    },
  ],
};

export function VisitorDirectoryPage() {
  const { data, isLoading, isError, refetch } = useVisitors();

  const columns = useMemo(() => visitorColumns, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Visitor Log</h1>
        <p className="text-muted-foreground mt-2">
          Monitor site access, scheduled visits, and active guests.
        </p>
      </div>

      <DataTable
        columns={columns}
        data={data?.items ?? []}
        pageCount={data?.total_pages ?? 0}
        totalRows={data?.total ?? 0}
        isLoading={isLoading}
        isError={isError}
        onRetry={refetch}
        config={visitorTableConfig}
      />
    </div>
  );
}
