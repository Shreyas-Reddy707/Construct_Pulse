import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useWorkers } from "@/modules/workers/hooks/useWorkers";
import { workerColumns } from "@/modules/workers/columns/workerColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const contractorWorkerTableConfig: DataTableConfig = {
  enableRowSelection: false,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search contractor workers..." }
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Active", value: "active" },
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

export default function ContractorRosterTab() {
  // Uses searchParams. The backend API handles the contractor filter 
  // via query params naturally if navigated here correctly.
  const { data, isLoading, isError, refetch } = useWorkers();

  const columns = useMemo(() => workerColumns, []);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Contractor Roster</h3>
        <p className="text-sm text-muted-foreground">
          All workers officially registered under this contracting organization.
        </p>
      </div>

      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <DataTable
          columns={columns}
          data={data?.items ?? []}
          pageCount={data?.total_pages ?? 0}
          totalRows={data?.total ?? 0}
          isLoading={isLoading}
          isError={isError}
          onRetry={refetch}
          config={contractorWorkerTableConfig}
        />
      </div>
    </div>
  );
}
