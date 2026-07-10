export interface Worker {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  department: string;
  current_site: string | null;
  status: "active" | "suspended" | "pending";
  created_at: string;
}

export interface WorkerDetail extends Worker {
  phone: string;
  emergency_contact: string | null;
  contractor_name: string;
  department_name: string;
}

// Ensure PaginatedResponse from data-table types is used
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
}
