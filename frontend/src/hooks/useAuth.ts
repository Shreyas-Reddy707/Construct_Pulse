import { useAuthStore } from "@/store/useAuthStore";
import { authService } from "@/services/authService";

export const useAuth = () => {
  const { user, isAuthenticated, isHydrated, setAuth, clearAuth, setHydrated } = useAuthStore();

  const checkAuthStatus = () => {
    return authService.isAuthenticated();
  };

  return {
    user,
    isAuthenticated,
    isHydrated,
    setAuth,
    clearAuth,
    setHydrated,
    checkAuthStatus,
  };
};
