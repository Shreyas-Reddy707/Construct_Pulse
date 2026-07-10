import type { Contractor, ContractorDetail } from "@/modules/contractors/types";

export interface BackendContractorResponse {
  id: string;
  name: string;
  company: string;
  status?: string | null;
  assigned_sites: string[];
  worker_count: number;
  contract_expiry?: string | null;
  created_at?: string;
  
  total_workers?: number;
  active_workers?: number;
  active_sites?: number;
  primary_contact_name?: string | null;
  primary_contact_phone?: string | null;
  primary_contact_email?: string | null;
  operational_status?: string | null;
  compliance_status?: string | null;
}

export function mapContractor(backendContractor: BackendContractorResponse): Contractor {
  return {
    id: backendContractor.id,
    name: backendContractor.name,
    company: backendContractor.company,
    status: (backendContractor.status?.toLowerCase() as Contractor["status"]) || "active",
    assigned_sites: backendContractor.assigned_sites || [],
    worker_count: backendContractor.worker_count || 0,
    contract_expiry: backendContractor.contract_expiry || new Date().toISOString(),
    created_at: backendContractor.created_at || new Date().toISOString(),
  };
}

export function mapContractorDetail(backendContractor: BackendContractorResponse): ContractorDetail {
  return {
    ...mapContractor(backendContractor),
    total_workers: backendContractor.total_workers || backendContractor.worker_count || 0,
    active_workers: backendContractor.active_workers || 0,
    active_sites: backendContractor.active_sites || backendContractor.assigned_sites?.length || 0,
    primary_contact_name: backendContractor.primary_contact_name || "Unknown",
    primary_contact_phone: backendContractor.primary_contact_phone || "",
    primary_contact_email: backendContractor.primary_contact_email || "",
    operational_status: (backendContractor.operational_status?.toLowerCase() as ContractorDetail["operational_status"]) || "active",
    compliance_status: (backendContractor.compliance_status?.toLowerCase() as ContractorDetail["compliance_status"]) || "review_pending",
  };
}
