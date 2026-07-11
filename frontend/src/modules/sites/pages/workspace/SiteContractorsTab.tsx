import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "@/components/data-table/DataTable";
import { useSiteAssignments } from "../../hooks/useSiteAssignments";
import { contractorColumns } from "@/modules/contractors/columns/contractorColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const siteContractorTableConfig: DataTableConfig = {
  enableRowSelection: false,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search contractors..." },
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Active", value: "active" },
        { label: "Suspended", value: "suspended" },
        { label: "Expired", value: "expired" },
      ],
    },
  ],
};

export default function SiteContractorsTab() {
  const { id } = useParams<{ id: string }>();
  const { data, isLoading, isError, refetch } = useSiteAssignments(id);

  const columns = useMemo(() => contractorColumns, []);
  const contractors = data?.contractors ?? [];

  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Active Contractors</h3>
        <p className="text-sm text-muted-foreground">
          Contracting organizations currently assigned to this site.
        </p>
      </div>

      <div className="bg-card shadow-sm border rounded-xl overflow-hidden">
        <DataTable
          columns={columns}
          data={contractors}
          pageCount={1}
          totalRows={contractors.length}
          isLoading={isLoading}
          isError={isError}
          onRetry={refetch}
          config={siteContractorTableConfig}
        />
      </div>
    </div>
  );
}
