import type { PaginatedResponse } from "@/components/data-table/types";

export interface Visitor {
  id: string;
  name: string;
  company: string;
  host: string;
  site: string;
  purpose: string;
  status: "scheduled" | "checked_in" | "checked_out" | "denied";
  check_in: string | null;
  check_out: string | null;
  created_at: string;
}

export type { PaginatedResponse };
