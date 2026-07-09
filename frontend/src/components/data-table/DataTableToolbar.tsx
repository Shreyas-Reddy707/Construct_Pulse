import type { Table } from "@tanstack/react-table";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "./DataTableViewOptions";
import { useDebouncedCallback } from "use-debounce";
import { useEffect, useState } from "react";
import type { DataTableConfig } from "./types";
import { DataTableFacetedFilter } from "./DataTableFacetedFilter";

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  globalFilter: string;
  onGlobalFilterChange: (value: string) => void;
  config?: DataTableConfig;
  getFilter: (id: string) => string | null;
  setFilter: (id: string, value: string | null) => void;
}

export function DataTableToolbar<TData>({
  table,
  globalFilter,
  onGlobalFilterChange,
  config,
  getFilter,
  setFilter,
}: DataTableToolbarProps<TData>) {
  const [inputValue, setInputValue] = useState(globalFilter);

  const debounced = useDebouncedCallback((value) => {
    onGlobalFilterChange(value);
  }, 300);

  useEffect(() => {
    setInputValue(globalFilter);
  }, [globalFilter]);

  const hasFilters = globalFilter.length > 0 || config?.filterableColumns?.some((col: any) => getFilter(col.id) !== null);

  const handleReset = () => {
    onGlobalFilterChange("");
    config?.filterableColumns?.forEach((col: any) => setFilter(col.id, null));
  };

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Search..."
          value={inputValue}
          onChange={(event) => {
            setInputValue(event.target.value);
            debounced(event.target.value);
          }}
          className="h-8 w-[150px] lg:w-[250px]"
        />
        {config?.filterableColumns?.map((filterCol: any) => {
          const column = table.getColumn(filterCol.id);
          if (!column) return null;
          return (
            <DataTableFacetedFilter
              key={filterCol.id}
              title={filterCol.title}
              options={filterCol.options}
              value={getFilter(filterCol.id)}
              onChange={(val) => setFilter(filterCol.id, val)}
            />
          );
        })}
        {hasFilters && (
          <Button
            variant="ghost"
            onClick={handleReset}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <X className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
      <div className="flex items-center gap-2">
        {config?.enableColumnVisibility && <DataTableViewOptions table={table} />}
      </div>
    </div>
  );
}
