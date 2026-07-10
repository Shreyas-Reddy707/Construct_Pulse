import type { Visitor } from "@/modules/visitors/types";

export interface BackendVisitorResponse {
  id: string;
  name: string;
  company: string;
  host_name?: string | null;
  site_name?: string | null;
  purpose?: string | null;
  status: string;
  check_in_time?: string | null;
  check_out_time?: string | null;
  created_at?: string;
}

export function mapVisitor(backendVisitor: BackendVisitorResponse): Visitor {
  return {
    id: backendVisitor.id,
    name: backendVisitor.name,
    company: backendVisitor.company,
    host: backendVisitor.host_name || "Unknown",
    site: backendVisitor.site_name || "Unknown",
    purpose: backendVisitor.purpose || "General",
    status: (backendVisitor.status?.toLowerCase() as Visitor["status"]) || "scheduled",
    check_in: backendVisitor.check_in_time || null,
    check_out: backendVisitor.check_out_time || null,
    created_at: backendVisitor.created_at || new Date().toISOString(),
  };
}
