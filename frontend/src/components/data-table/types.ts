export interface FilterOption {
  label: string;
  value: string;
}

export interface FilterDefinition {
  id: string;
  title: string;
  options: FilterOption[];
}

export interface DataTableConfig {
  pageSizes?: number[];
  mobileBehavior?: "scroll" | "cards";
  searchableFields?: { id: string; placeholder: string }[];
  filterableColumns?: FilterDefinition[];
  enableRowSelection?: boolean;
  enableColumnVisibility?: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}
