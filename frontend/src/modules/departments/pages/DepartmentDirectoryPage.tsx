import { useMemo } from "react";
import { DataTable } from "@/components/data-table/DataTable";
import { useDepartments } from "../hooks/useDepartments";
import { departmentColumns } from "../columns/departmentColumns";
import type { DataTableConfig } from "@/components/data-table/types";

const departmentTableConfig: DataTableConfig = {
  enableRowSelection: true,
  enableColumnVisibility: true,
  mobileBehavior: "scroll",
  searchableFields: [
    { id: "search", placeholder: "Search departments..." },
  ],
  filterableColumns: [
    {
      id: "status",
      title: "Status",
      options: [
        { label: "Active", value: "active" },
        { label: "Inactive", value: "inactive" },
        { label: "Under Review", value: "under_review" },
      ],
    },
  ],
};

export function DepartmentDirectoryPage() {
  const { data, isLoading, isError, refetch } = useDepartments();

  const columns = useMemo(() => departmentColumns, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Department Directory</h1>
        <p className="text-muted-foreground mt-2">
          Manage departments, staffing levels, and site assignments.
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
        config={departmentTableConfig}
      />
    </div>
  );
}
