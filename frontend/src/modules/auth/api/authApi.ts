import { apiClient } from "@/api/client";
import type { AuthResponse, User } from "../types";
import type { LoginFormValues } from "../validation";
import { authService } from "@/services/authService";

export const authApi = {
  login: async (credentials: LoginFormValues): Promise<AuthResponse> => {
    // We send form data according to WS1 standard (OAuth2PasswordRequestForm usually takes username/password)
    // Assuming backend takes JSON or form-data depending on implementation. 
    // Standard OAuth2 FastAPI expects form-data for login:
    const formData = new FormData();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);
    
    const response = await apiClient.post<AuthResponse>("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    });
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>("/users/me");
    return response.data;
  },

  logout: async (): Promise<void> => {
    authService.removeToken();
    // In many SaaS apps, we also invalidate token on backend here if applicable
    // await apiClient.post("/auth/logout");
  },
};
