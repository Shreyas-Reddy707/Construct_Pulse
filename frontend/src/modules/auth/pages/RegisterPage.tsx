import { useSearchParams, Link, Navigate } from "react-router-dom";
import { RegisterForm } from "../components/RegisterForm";
import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent } from "@/components/ui/card";
import { QrCode, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export function RegisterPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  if (!token) {
    return (
      <div className="w-full max-w-md flex flex-col items-center justify-center space-y-6">
        <Card className="w-full shadow-lg border-muted/40">
          <CardContent className="pt-10 pb-8 flex flex-col items-center text-center space-y-4">
            <div className="h-20 w-20 bg-muted/50 rounded-full flex items-center justify-center text-muted-foreground mb-2">
              <QrCode size={40} />
            </div>
            <h2 className="text-xl font-semibold tracking-tight">Missing Site Token</h2>
            <p className="text-muted-foreground text-sm max-w-[280px]">
              To register for site access, you must scan the QR code located at the site entrance.
            </p>
          </CardContent>
        </Card>
        
        <Button variant="ghost" asChild>
          <Link to="/login" className="flex items-center text-muted-foreground hover:text-foreground">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Login
          </Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="w-full max-w-md flex flex-col items-center justify-center space-y-6">
      <RegisterForm qrToken={token} />
      
      <Button variant="ghost" asChild>
        <Link to="/login" className="flex items-center text-muted-foreground hover:text-foreground">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Login
        </Link>
      </Button>
    </div>
  );
}
