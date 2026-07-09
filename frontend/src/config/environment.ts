export const env = {
  apiUrl: (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000/api/v1",
  appName: (import.meta.env.VITE_APP_NAME as string) || "ConstructPulse",
  enableDevTools: import.meta.env.VITE_ENABLE_DEVTOOLS === "true",
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
} as const;
