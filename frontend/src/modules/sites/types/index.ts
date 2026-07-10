import type { PaginatedResponse } from "@/components/data-table/types";

export interface Site {
  id: string;
  name: string;
  code: string;
  status: "pre-construction" | "active" | "paused" | "completed" | "handover";
  supervisor: string;
  municipality: string;
  current_occupancy: number;
  max_occupancy: number;
  created_at: string;
}

export interface SiteDetail extends Site {
  project_manager_name: string;
}

export type { PaginatedResponse };
