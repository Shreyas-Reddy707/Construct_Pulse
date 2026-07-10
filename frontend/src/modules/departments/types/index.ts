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

export type { PaginatedResponse };
