import { apiClient } from "@/api/client";
import type { AuthResponse, User } from "../types";
import type { LoginFormValues, RegistrationFormValues } from "../validation";
import { authService } from "@/services/authService";
import { env } from "@/config/environment";

export const authApi = {
  login: async (credentials: LoginFormValues): Promise<AuthResponse> => {
    let idToken = "";

    const useDemoAuth = env.enableDemoAuth;

    if (useDemoAuth) {
      // The backend DEMO_AUTH mode expects "DEMO_TOKEN_" + identifier. 
      idToken = `DEMO_TOKEN_${credentials.phone}`;
    } else {
      // FUTURE PRODUCTION REPLACEMENT:
      // const confirmationResult = await signInWithPhoneNumber(auth, credentials.phone, appVerifier);
      // const result = await confirmationResult.confirm(credentials.otp);
      // idToken = await result.user.getIdToken();
      throw new Error("Real Firebase Auth is not yet configured in this MVP.");
    }

    const response = await apiClient.post<AuthResponse>("/auth/login", {
      token: idToken,
    });
    
    return response.data;
  },

  registerRequest: async (data: RegistrationFormValues & { qr_token: string }): Promise<void> => {
    await apiClient.post("/register/request", data);
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>("/users/me");
    return response.data;
  },

  logout: async (): Promise<void> => {
    authService.removeToken();
  },
};

