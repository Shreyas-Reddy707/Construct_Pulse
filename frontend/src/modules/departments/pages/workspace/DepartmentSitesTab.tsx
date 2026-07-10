import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "@/components/data-table/DataTable";
import { useSites } from "@/modules/sites/hooks/useSites";
import { siteColumns } from "@/modules/sites/columns/siteColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const departmentSiteTableConfig: DataTableConfig = {
  enableRowSelection: false,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search deployed sites..." }
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

export default function DepartmentSitesTab() {
  const { id } = useParams<{ id: string }>();

  // Use explicit parameterized filtering to prevent URL dependency
  const { data, isLoading, isError, refetch } = useSites({
    department_id: id || null,
  });

  const columns = useMemo(() => siteColumns, []);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Deployed Sites</h3>
        <p className="text-sm text-muted-foreground">
          Geographic locations where this department's resources are currently deployed.
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
          config={departmentSiteTableConfig}
        />
      </div>
    </div>
  );
}
