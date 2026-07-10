import type { Site, SiteDetail } from "@/modules/sites/types";

export interface BackendSiteResponse {
  id: string;
  name: string;
  code?: string | null;
  status: string;
  supervisor?: string | null;
  municipality?: string | null;
  current_occupancy: number;
  max_occupancy: number;
  created_at?: string;
  project_manager_name?: string | null;
}

export function mapSite(backendSite: BackendSiteResponse): Site {
  return {
    id: backendSite.id,
    name: backendSite.name,
    code: backendSite.code || "",
    status: (backendSite.status?.toLowerCase() as Site["status"]) || "active",
    supervisor: backendSite.supervisor || "Unassigned",
    municipality: backendSite.municipality || "Unknown",
    current_occupancy: backendSite.current_occupancy || 0,
    max_occupancy: backendSite.max_occupancy || 0,
    created_at: backendSite.created_at || new Date().toISOString(),
  };
}

export function mapSiteDetail(backendSite: BackendSiteResponse): SiteDetail {
  return {
    ...mapSite(backendSite),
    project_manager_name: backendSite.project_manager_name || "Unassigned",
  };
}
