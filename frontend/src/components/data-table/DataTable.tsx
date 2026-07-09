import * as React from "react";
import type {
  ColumnDef,
  VisibilityState,
} from "@tanstack/react-table";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { DataTableToolbar } from "./DataTableToolbar";
import { DataTablePagination } from "./DataTablePagination";
import { DataTableSkeleton } from "./DataTableSkeleton";
import { DataTableEmpty } from "./DataTableEmpty";
import { DataTableError } from "./DataTableError";
import { useDataTable } from "./useDataTable";
import type { DataTableConfig } from "./types";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  pageCount: number;
  totalRows: number;
  isLoading?: boolean;
  isError?: boolean;
  onRetry?: () => void;
  config?: DataTableConfig;
}

export function DataTable<TData, TValue>({
  columns,
  data,
  pageCount,
  totalRows,
  isLoading,
  isError,
  onRetry,
  config,
}: DataTableProps<TData, TValue>) {
  const {
    pagination,
    sorting,
    globalFilter,
    onPaginationChange,
    onSortingChange,
    onGlobalFilterChange,
    setFilter,
    getFilter,
  } = useDataTable();

  const [rowSelection, setRowSelection] = React.useState({});
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});

  const table = useReactTable({
    data,
    columns,
    pageCount,
    state: {
      pagination,
      sorting,
      rowSelection,
      columnVisibility,
    },
    enableRowSelection: config?.enableRowSelection,
    onRowSelectionChange: setRowSelection,
    onSortingChange: onSortingChange,
    onPaginationChange: onPaginationChange,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
  });

  return (
    <div className="space-y-4">
      <DataTableToolbar
        table={table}
        globalFilter={globalFilter}
        onGlobalFilterChange={onGlobalFilterChange}
        config={config}
        getFilter={getFilter}
        setFilter={setFilter}
      />
      
      {isLoading ? (
        <DataTableSkeleton columnCount={columns.length} />
      ) : isError ? (
        <div className="rounded-md border">
          <Table>
            <TableBody>
              <DataTableError columnCount={columns.length} onRetry={onRetry} />
            </TableBody>
          </Table>
        </div>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    return (
                      <TableHead key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableHead>
                    );
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows?.length ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <DataTableEmpty columnCount={columns.length} />
              )}
            </TableBody>
          </Table>
        </div>
      )}

      {!isLoading && !isError && (
        <DataTablePagination table={table} totalRows={totalRows} />
      )}
    </div>
  );
}
