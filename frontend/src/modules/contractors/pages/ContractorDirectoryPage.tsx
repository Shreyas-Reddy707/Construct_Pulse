import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useContractors } from "../hooks/useContractors";
import { contractorColumns } from "../columns/contractorColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const contractorTableConfig: DataTableConfig = {
  enableRowSelection: true,
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

export function ContractorDirectoryPage() {
  const { data, isLoading, isError, refetch } = useContractors();

  const columns = useMemo(() => contractorColumns, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Contractor Directory</h1>
        <p className="text-muted-foreground mt-2">
          Manage external contractors, contracts, and site assignments.
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
        config={contractorTableConfig}
      />
    </div>
  );
}
