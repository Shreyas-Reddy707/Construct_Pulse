import { create } from "zustand";
import { authService } from "@/services/authService";

interface User {
  id: string;
  email: string;
  name?: string;
  role: string;
  company_id: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isHydrated: boolean;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  setHydrated: (state: boolean) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isHydrated: false,
  setAuth: (user, token) => {
    authService.saveToken(token);
    set({ user, isAuthenticated: true });
  },
  clearAuth: () => {
    authService.removeToken();
    set({ user: null, isAuthenticated: false });
  },
  setHydrated: (state) => set({ isHydrated: state }),
}));
