import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useWorkers } from "../hooks/useWorkers";
import { workerColumns } from "../columns/workerColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const workerTableConfig: DataTableConfig = {
  enableRowSelection: true,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search workers by name or email..." }
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Approved", value: "approved" },
        { label: "Suspended", value: "suspended" },
        { label: "Pending", value: "pending" },
      ],
    },
    {
      id: "role",
      title: "Role",
      options: [
        { label: "Laborer", value: "laborer" },
        { label: "Foreman", value: "foreman" },
        { label: "Supervisor", value: "supervisor" },
        { label: "Operator", value: "operator" },
      ],
    },
  ],
};

export function WorkerDirectoryPage() {
  const { data, isLoading, isError, refetch } = useWorkers();

  // Memoize columns to prevent infinite rerenders in TanStack
  const columns = useMemo(() => workerColumns, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Worker Directory</h1>
        <p className="text-muted-foreground mt-2">
          Manage site personnel, roles, and access status.
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
        config={workerTableConfig}
      />
    </div>
  );
}
