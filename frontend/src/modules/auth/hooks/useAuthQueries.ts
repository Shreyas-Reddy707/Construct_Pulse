import { useMutation, useQuery } from "@tanstack/react-query";
import { authApi } from "../api/authApi";
import { useAuth } from "@/hooks/useAuth";

export const authKeys = {
  me: ["auth", "me"] as const,
};

export function useLoginMutation() {
  const { setAuth } = useAuth();

  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      setAuth(data.user, data.access_token);
    },
  });
}

export function useCurrentUser() {
  const { isAuthenticated } = useAuth();
  
  return useQuery({
    queryKey: authKeys.me,
    queryFn: authApi.me,
    enabled: isAuthenticated,
    staleTime: Infinity, // User session data doesn't frequently change
  });
}
