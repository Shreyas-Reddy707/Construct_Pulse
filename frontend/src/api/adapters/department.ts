import type { Department, DepartmentDetail } from "@/modules/departments/types";

export interface BackendDepartmentResponse {
  id: string;
  name: string;
  department_code?: string | null;
  status?: string | null;
  head?: string | null;
  head_name?: string | null;
  head_phone?: string | null;
  head_email?: string | null;
  worker_count: number;
  total_workers: number;
  active_sites: number;
  assigned_sites: string[];
  created_at?: string;
}

export function mapDepartment(backendDepartment: BackendDepartmentResponse): Department {
  return {
    id: backendDepartment.id,
    name: backendDepartment.name,
    status: (backendDepartment.status?.toLowerCase() as Department["status"]) || "active",
    head: backendDepartment.head || backendDepartment.head_name || "Unassigned",
    worker_count: backendDepartment.worker_count || 0,
    assigned_sites: backendDepartment.assigned_sites || [],
    created_at: backendDepartment.created_at || new Date().toISOString(),
  };
}

export function mapDepartmentDetail(backendDepartment: BackendDepartmentResponse): DepartmentDetail {
  return {
    ...mapDepartment(backendDepartment),
    department_code: backendDepartment.department_code || "",
    head_name: backendDepartment.head_name || backendDepartment.head || "Unassigned",
    head_phone: backendDepartment.head_phone || "",
    head_email: backendDepartment.head_email || "",
    total_workers: backendDepartment.total_workers || backendDepartment.worker_count || 0,
    active_sites: backendDepartment.active_sites || backendDepartment.assigned_sites?.length || 0,
  };
}
