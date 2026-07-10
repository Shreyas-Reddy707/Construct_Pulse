import type { PaginatedResponse } from "@/components/data-table/types";

export interface Department {
  id: string;
  name: string;
  status: "active" | "inactive" | "under_review";
  head: string;
  worker_count: number;
  assigned_sites: string[];
  created_at: string;
}

export interface DepartmentDetail extends Department {
  department_code: string;
  head_name: string;
  head_phone: string;
  head_email: string;
  total_workers: number;
  active_sites: number;
}

export type { PaginatedResponse };
