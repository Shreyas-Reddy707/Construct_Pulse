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

export interface ContractorDetail extends Contractor {
  total_workers: number;
  active_workers: number;
  active_sites: number;
  primary_contact_name: string;
  primary_contact_phone: string;
  primary_contact_email: string;
  operational_status: "active" | "suspended" | "expired";
  compliance_status: "compliant" | "non_compliant" | "review_pending";
}

export type { PaginatedResponse };
