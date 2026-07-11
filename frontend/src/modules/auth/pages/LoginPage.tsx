import { LoginForm } from "../components/LoginForm";
import { useAuth } from "@/hooks/useAuth";
import { Navigate } from "react-router-dom";

export function LoginPage() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="w-full max-w-sm flex flex-col gap-6">
      <LoginForm />
      
      <p className="text-center text-sm text-muted-foreground px-6">
        Need to register for site access? Please scan the QR code located at your site entrance to begin the registration process.
      </p>
    </div>
  );
}
