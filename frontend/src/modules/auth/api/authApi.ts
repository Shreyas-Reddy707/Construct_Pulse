import { apiClient } from "@/api/client";
import type { AuthResponse, User } from "../types";
import type { LoginFormValues } from "../validation";
import { authService } from "@/services/authService";
import { env } from "@/config/environment";

export const authApi = {
  login: async (credentials: LoginFormValues): Promise<AuthResponse> => {
    let idToken = "";

    // In a real production app, we would authenticate with Firebase Client SDK here:
    // const userCredential = await signInWithEmailAndPassword(auth, credentials.email, credentials.password);
    // idToken = await userCredential.user.getIdToken();
    
    // For MVP with DEMO_AUTH enabled on the backend, we bypass real Firebase
    const useDemoAuth = env.enableDemoAuth;

    if (useDemoAuth) {
      // The backend DEMO_AUTH mode expects "DEMO_TOKEN_" + identifier. 
      // We map the login email directly to this for demo purposes.
      idToken = `DEMO_TOKEN_${credentials.email}`;
    } else {
      // FUTURE PRODUCTION REPLACEMENT:
      // const userCredential = await signInWithEmailAndPassword(auth, credentials.email, credentials.password);
      // idToken = await userCredential.user.getIdToken();
      throw new Error("Real Firebase Auth is not yet configured in this MVP.");
    }

    const response = await apiClient.post<AuthResponse>("/auth/login", {
      token: idToken,
    });
    
    return response.data;
  },

  me: async (): Promise<User> => {
    const response = await apiClient.get<User>("/users/me");
    return response.data;
  },

  logout: async (): Promise<void> => {
    authService.removeToken();
  },
};
