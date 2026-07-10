import type { PaginatedResponse as FrontendPaginatedResponse } from "@/components/data-table/types";

// The backend's standard generic pagination response shape
export interface BackendPaginatedResponse<T> {
  data: T[];
  metadata: {
    total_records: number;
    skip: number;
    limit: number;
    page_size: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
  };
}

// The custom attendance workspace pagination response shape
export interface BackendAttendancePageResponse<T> {
  items: T[];
  total_records: number;
  skip: number;
  limit: number;
}

/**
 * Normalizes the backend's standard pagination envelope into the frontend's expected shape.
 */
export function mapPagination<TBackend, TFrontend>(
  response: BackendPaginatedResponse<TBackend>,
  mapper: (item: TBackend) => TFrontend
): FrontendPaginatedResponse<TFrontend> {
  const limit = response.metadata.limit > 0 ? response.metadata.limit : 1;
  return {
    items: response.data.map(mapper),
    total: response.metadata.total_records,
    page: Math.floor(response.metadata.skip / limit) + 1,
    size: response.metadata.limit,
    total_pages: response.metadata.total_pages,
  };
}

/**
 * Normalizes the backend's attendance pagination envelope into the frontend's expected shape.
 */
export function mapAttendancePagination<TBackend, TFrontend>(
  response: BackendAttendancePageResponse<TBackend>,
  mapper: (item: TBackend) => TFrontend
): FrontendPaginatedResponse<TFrontend> {
  const limit = response.limit > 0 ? response.limit : 10;
  return {
    items: response.items.map(mapper),
    total: response.total_records,
    page: Math.floor(response.skip / limit) + 1,
    size: limit,
    total_pages: Math.ceil(response.total_records / limit) || 1,
  };
}
