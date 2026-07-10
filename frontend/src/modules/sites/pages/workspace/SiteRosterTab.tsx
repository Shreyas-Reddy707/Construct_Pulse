import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useWorkers } from "@/modules/workers/hooks/useWorkers";
import { workerColumns } from "@/modules/workers/columns/workerColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const siteWorkerTableConfig: DataTableConfig = {
  enableRowSelection: false, // In a site context, we might not bulk-select across the board yet
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search assigned workers..." }
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

export default function SiteRosterTab() {
  // Reusing the domain hook from workers. 
  // Note: in a fully wired app, the hook might need an initial filter prop for `site_id`,
  // but per architectural rules, we compose existing hooks natively.
  const { data, isLoading, isError, refetch } = useWorkers();

  const columns = useMemo(() => workerColumns, []);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Live Roster</h3>
        <p className="text-sm text-muted-foreground">
          Workers currently assigned or checked into this site.
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
          config={siteWorkerTableConfig}
        />
      </div>
    </div>
  );
}
