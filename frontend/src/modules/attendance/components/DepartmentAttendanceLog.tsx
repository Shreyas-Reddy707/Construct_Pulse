import { useMemo } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "@/components/data-table/DataTable";
import { useDepartmentAttendanceHistory } from "../hooks/useDepartmentAttendanceHistory";
import type { AttendanceLog } from "../types";
import { Badge } from "@/components/ui/badge";
import type { DataTableConfig } from "@/components/data-table/types";

interface DepartmentAttendanceLogProps {
  departmentId: string;
}

const departmentAttendanceConfig: DataTableConfig = {
  enableRowSelection: false,
  enableColumnVisibility: false,
  mobileBehavior: "scroll",
  searchableFields: [],
  filterableColumns: [
    {
      id: "scan_type",
      title: "Action",
      options: [
        { label: "Check In", value: "check_in" },
        { label: "Check Out", value: "check_out" },
      ],
    },
  ],
};

export function DepartmentAttendanceLog({ departmentId }: DepartmentAttendanceLogProps) {
  const { data, isLoading, isError, refetch } = useDepartmentAttendanceHistory(departmentId);

  const columns = useMemo<ColumnDef<AttendanceLog>[]>(
    () => [
      {
        accessorKey: "timestamp",
        header: "Time",
        cell: ({ row }) => {
          const timestamp = row.getValue("timestamp") as string;
          return new Intl.DateTimeFormat("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit",
          }).format(new Date(timestamp));
        },
      },
      {
        accessorKey: "worker_id",
        header: "Worker",
      },
      {
        accessorKey: "site_id",
        header: "Site",
      },
      {
        accessorKey: "scan_type",
        header: "Action",
        cell: ({ row }) => {
          const type = row.getValue("scan_type") as string;
          return (
            <Badge variant={type === "check_in" ? "default" : "secondary"}>
              {type === "check_in" ? "Check In" : "Check Out"}
            </Badge>
          );
        },
      },
    ],
    []
  );

  return (
    <DataTable
      columns={columns}
      data={data?.items ?? []}
      pageCount={data?.total_pages ?? 0}
      totalRows={data?.total ?? 0}
      isLoading={isLoading}
      isError={isError}
      onRetry={refetch}
      config={departmentAttendanceConfig}
    />
  );
}
