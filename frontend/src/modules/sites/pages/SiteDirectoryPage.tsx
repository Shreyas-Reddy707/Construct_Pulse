import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useSites } from "../hooks/useSites";
import { siteColumns } from "../columns/siteColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const siteTableConfig: DataTableConfig = {
  enableRowSelection: true,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search sites by name or code..." }
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Active", value: "active" },
        { label: "Pre-construction", value: "pre-construction" },
        { label: "Paused", value: "paused" },
        { label: "Completed", value: "completed" },
        { label: "Handover", value: "handover" },
      ],
    }
  ],
};

export function SiteDirectoryPage() {
  const { data, isLoading, isError, refetch } = useSites();

  // Memoize columns to prevent infinite rerenders in TanStack
  const columns = useMemo(() => siteColumns, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Site Directory</h1>
        <p className="text-muted-foreground mt-2">
          Manage construction sites, occupancy, and operational status.
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
        config={siteTableConfig}
      />
    </div>
  );
}
