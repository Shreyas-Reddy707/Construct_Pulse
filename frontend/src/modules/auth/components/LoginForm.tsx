import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema } from "../validation";
import type { LoginFormValues } from "../validation";
import { useLoginMutation } from "../hooks/useAuthQueries";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Loader2, ArrowRight, ArrowLeft } from "lucide-react";
import { toast } from "sonner";

export function LoginForm() {
  const [step, setStep] = useState<1 | 2>(1);
  const loginMutation = useLoginMutation();

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      phone: "",
      otp: "",
    },
  });

  const handleSendCode = async () => {
    const isValid = await form.trigger("phone");
    if (isValid) {
      // In production, this would trigger Firebase signInWithPhoneNumber
      toast.success("Verification code sent!");
      setStep(2);
    }
  };

  const onSubmit = (data: LoginFormValues) => {
    if (step === 1) {
      handleSendCode();
      return;
    }
    
    if (!data.otp || data.otp.length !== 6) {
      form.setError("otp", { message: "OTP must be 6 digits" });
      return;
    }

    loginMutation.mutate(data);
  };

  return (
    <Card className="w-full max-w-sm shadow-lg border-muted/40">
      <CardHeader className="space-y-2">
        <CardTitle className="text-2xl font-semibold tracking-tight text-center">
          {step === 1 ? "Welcome Back" : "Verify Phone"}
        </CardTitle>
        <CardDescription className="text-center">
          {step === 1 ? "Enter your phone number to continue." : "Enter the 6-digit code sent to your phone."}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            
            {step === 1 && (
              <FormField
                control={form.control}
                name="phone"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="sr-only">Phone Number</FormLabel>
                    <FormControl>
                      <Input
                        type="tel"
                        inputMode="tel"
                        placeholder="+1 (555) 000-0000"
                        className="h-12 text-base text-center tracking-wide"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className="text-center" />
                  </FormItem>
                )}
              />
            )}

            {step === 2 && (
              <FormField
                control={form.control}
                name="otp"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="sr-only">Verification Code</FormLabel>
                    <FormControl>
                      <Input
                        type="text"
                        inputMode="numeric"
                        placeholder="123456"
                        maxLength={6}
                        className="h-14 text-base text-center tracking-[0.5em] text-2xl font-semibold"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className="text-center" />
                  </FormItem>
                )}
              />
            )}

            <div className="flex gap-3 pt-2">
              {step === 2 && (
                <Button
                  type="button"
                  variant="outline"
                  className="h-12 w-12 p-0 flex-shrink-0"
                  onClick={() => setStep(1)}
                  disabled={loginMutation.isPending}
                >
                  <ArrowLeft className="h-5 w-5 text-muted-foreground" />
                </Button>
              )}
              
              <Button
                type="submit"
                className="h-12 flex-1 text-base font-medium transition-all"
                disabled={loginMutation.isPending}
              >
                {loginMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Authenticating...
                  </>
                ) : step === 1 ? (
                  <>
                    Send Code
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </>
                ) : (
                  "Verify & Log In"
                )}
              </Button>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
