import type { PaginatedResponse } from "@/components/data-table/types";

export interface Contractor {
  id: string;
  name: string;
  company: string;
  status: "active" | "suspended" | "expired";
  assigned_sites: string[];
  worker_count: number;
  contract_expiry: string;
  created_at: string;
}

export type { PaginatedResponse };
