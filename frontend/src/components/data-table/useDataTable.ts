import { useSearchParams } from "react-router-dom";
import { useCallback, useMemo } from "react";
import type { PaginationState, SortingState } from "@tanstack/react-table";

export function useDataTable() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Parse pagination from URL
  const pageIndex = Number(searchParams.get("page") ?? "1") - 1;
  const pageSize = Number(searchParams.get("limit") ?? "20");
  const pagination: PaginationState = useMemo(() => ({ pageIndex, pageSize }), [pageIndex, pageSize]);

  // Parse sorting from URL
  const sortBy = searchParams.get("sort_by");
  const sortOrder = searchParams.get("sort_order");
  const sorting: SortingState = useMemo(
    () => (sortBy ? [{ id: sortBy, desc: sortOrder === "desc" }] : []),
    [sortBy, sortOrder]
  );

  // Parse search from URL
  const globalFilter = searchParams.get("search") ?? "";

  // Set URL Params Helper
  const updateUrl = useCallback(
    (updates: Record<string, string | null>) => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        Object.entries(updates).forEach(([key, value]) => {
          if (value === null || value === "") {
            next.delete(key);
          } else {
            next.set(key, value);
          }
        });
        return next;
      }, { replace: true });
    },
    [setSearchParams]
  );

  const onPaginationChange = useCallback(
    (updater: PaginationState | ((old: PaginationState) => PaginationState)) => {
      const next = typeof updater === "function" ? updater(pagination) : updater;
      updateUrl({
        page: (next.pageIndex + 1).toString(),
        limit: next.pageSize.toString(),
      });
    },
    [pagination, updateUrl]
  );

  const onSortingChange = useCallback(
    (updater: SortingState | ((old: SortingState) => SortingState)) => {
      const next = typeof updater === "function" ? updater(sorting) : updater;
      if (next.length === 0) {
        updateUrl({ sort_by: null, sort_order: null, page: "1" });
      } else {
        updateUrl({
          sort_by: next[0].id,
          sort_order: next[0].desc ? "desc" : "asc",
          page: "1",
        });
      }
    },
    [sorting, updateUrl]
  );

  const onGlobalFilterChange = useCallback(
    (value: string) => {
      updateUrl({ search: value || null, page: "1" });
    },
    [updateUrl]
  );

  const setFilter = useCallback(
    (columnId: string, value: string | null) => {
      updateUrl({ [columnId]: value, page: "1" });
    },
    [updateUrl]
  );

  const getFilter = useCallback(
    (columnId: string) => {
      return searchParams.get(columnId);
    },
    [searchParams]
  );

  return {
    pagination,
    sorting,
    globalFilter,
    onPaginationChange,
    onSortingChange,
    onGlobalFilterChange,
    setFilter,
    getFilter,
    searchParams,
  };
}
