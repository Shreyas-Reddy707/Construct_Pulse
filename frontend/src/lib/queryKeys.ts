export const queryKeys = {
  dashboard: {
    summary: ["dashboard", "summary"] as const,
    trends: ["dashboard", "trends"] as const,
  },
  users: {
    all: ["users"] as const,
    list: (filters: Record<string, any>) => ["users", "list", filters] as const,
    detail: (id: string) => ["users", "detail", id] as const,
  },
  sites: {
    all: ["sites"] as const,
    list: (filters: Record<string, any>) => ["sites", "list", filters] as const,
  },
  attendance: {
    report: (filters: Record<string, any>) => ["attendance", "report", filters] as const,
  },
  occupancy: {
    live: (siteId: string) => ["occupancy", "live", siteId] as const,
  },
  departments: {
    all: ["departments"] as const,
  },
  contractors: {
    all: ["contractors"] as const,
  },
};
