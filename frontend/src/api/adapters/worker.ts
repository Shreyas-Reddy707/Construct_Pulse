import type { Worker, WorkerDetail } from "@/modules/workers/types";

export interface BackendUserResponse {
  id: string;
  name: string;
  phone_number: string;
  role: string;
  status: string;
  department_name?: string | null;
  contractor_name?: string | null;
  created_at?: string;
  assigned_site_names?: string | null;
}

export interface BackendWorkerDetailResponse {
  id: string;
  first_name?: string | null;
  last_name?: string | null;
  badge_id?: string | null;
  status: string;
  phone?: string | null;
  emergency_contact?: string | null;
  department?: { id: string; name: string } | null;
  contractor?: { id: string; name: string } | null;
}

export function mapWorker(backendWorker: BackendUserResponse): Worker {
  const parts = backendWorker.name ? backendWorker.name.split(" ") : ["", ""];
  const firstName = parts[0] || "Unknown";
  const lastName = parts.slice(1).join(" ") || "";

  return {
    id: backendWorker.id,
    first_name: firstName,
    last_name: lastName,
    email: backendWorker.phone_number || "", // Fallback as phone is required, email isn't in backend
    role: backendWorker.role || "worker",
    department: backendWorker.department_name || "Unassigned",
    current_site: backendWorker.assigned_site_names || null,
    status: (backendWorker.status?.toLowerCase() as Worker["status"]) || "active",
    created_at: backendWorker.created_at || new Date().toISOString(),
  };
}

export function mapWorkerDetail(backendWorker: BackendWorkerDetailResponse): WorkerDetail {
  return {
    id: backendWorker.id,
    first_name: backendWorker.first_name || "Unknown",
    last_name: backendWorker.last_name || "",
    email: backendWorker.phone || "", // Fallback email to phone
    role: "worker", // Not in detail response
    department: backendWorker.department?.name || "Unassigned",
    current_site: null, // Not in detail response
    status: (backendWorker.status?.toLowerCase() as Worker["status"]) || "active",
    created_at: new Date().toISOString(), // Not in detail response
    phone: backendWorker.phone || "",
    emergency_contact: backendWorker.emergency_contact || null,
    contractor_name: backendWorker.contractor?.name || "Unassigned",
    department_name: backendWorker.department?.name || "Unassigned",
  };
}
