import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useContractors } from "@/modules/contractors/hooks/useContractors";
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
  // Reusing existing hook directly
  const { data, isLoading, isError, refetch } = useContractors();

  const columns = useMemo(() => contractorColumns, []);

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
          data={data?.items ?? []}
          pageCount={data?.total_pages ?? 0}
          totalRows={data?.total ?? 0}
          isLoading={isLoading}
          isError={isError}
          onRetry={refetch}
          config={siteContractorTableConfig}
        />
      </div>
    </div>
  );
}
