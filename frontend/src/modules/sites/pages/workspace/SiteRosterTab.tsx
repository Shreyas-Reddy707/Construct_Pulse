import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "@/components/data-table/DataTable";
import { useSiteAssignments } from "../../hooks/useSiteAssignments";
import { workerColumns } from "@/modules/workers/columns/workerColumns";
import { AssignWorkerDialog } from "../../components/workspace/AssignWorkerDialog";
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
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, isError, refetch } = useSiteAssignments(id);

  const columns = useMemo(() => workerColumns, []);
  const workers = data?.workers ?? [];

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="font-semibold tracking-tight text-lg">Live Roster</h3>
          <p className="text-sm text-muted-foreground">
            Workers currently assigned to this site.
          </p>
        </div>
        <AssignWorkerDialog siteId={id!} />
      </div>

      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <DataTable
          columns={columns}
          data={workers}
          pageCount={1}
          totalRows={workers.length}
          isLoading={isLoading}
          isError={isError}
          onRetry={refetch}
          config={siteWorkerTableConfig}
        />
      </div>
    </div>
  );
}
