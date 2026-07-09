import { useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { authApi } from "@/modules/auth/api/authApi";
import { authService } from "@/services/authService";

export function useAppBootstrap() {
  const { setHydrated, setAuth, clearAuth } = useAuth();

  useEffect(() => {
    let mounted = true;

    async function bootstrap() {
      const token = authService.getToken();

      if (!token) {
        if (mounted) setHydrated(true);
        return;
      }

      try {
        const user = await authApi.me();
        if (mounted) {
          setAuth(user, token);
          setHydrated(true);
        }
      } catch (error) {
        if (mounted) {
          clearAuth();
          setHydrated(true);
        }
      }
    }

    bootstrap();

    return () => {
      mounted = false;
    };
  }, [setHydrated, setAuth, clearAuth]);
}
