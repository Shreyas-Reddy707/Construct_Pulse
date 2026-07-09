import axios, { AxiosError } from "axios";
import { env } from "@/config/environment";
import { authService } from "@/services/authService";
import { ApiError } from "@/lib/ApiError";
import { toast } from "sonner";
import { useAuthStore } from "@/store/useAuthStore";

export const apiClient = axios.create({
  baseURL: env.apiUrl,
  timeout: 15000,
});

apiClient.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle 401 Unauthorized globally
      useAuthStore.getState().clearAuth();
      toast.error("Session expired. Please log in again.");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    // Convert backend DomainExceptions into standardized frontend ApiError
    let message = "An unexpected error occurred.";
    let details: unknown = null;

    if (error.response?.data) {
      const data = error.response.data as any;
      if (data.detail) {
        message = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
        details = data.detail;
      } else if (data.message) {
        message = data.message;
      }
    } else if (error.message) {
      message = error.message;
    }

    const apiError = new ApiError(
      message,
      error.response?.status || 500,
      details,
      error
    );

    return Promise.reject(apiError);
  }
);
