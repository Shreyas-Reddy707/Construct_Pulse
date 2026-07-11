import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { registrationSchema } from "../validation";
import type { RegistrationFormValues } from "../validation";
import { useRegisterMutation } from "../hooks/useAuthQueries";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Loader2, CheckCircle2 } from "lucide-react";

interface RegisterFormProps {
  qrToken: string;
}

export function RegisterForm({ qrToken }: RegisterFormProps) {
  const registerMutation = useRegisterMutation();

  const form = useForm<RegistrationFormValues>({
    resolver: zodResolver(registrationSchema),
    defaultValues: {
      full_name: "",
      phone_number: "",
      identity_type: "WORKER",
    },
  });

  const onSubmit = (data: RegistrationFormValues) => {
    registerMutation.mutate({
      ...data,
      qr_token: qrToken,
    });
  };

  if (registerMutation.isSuccess) {
    return (
      <Card className="w-full max-w-md shadow-lg border-muted/40">
        <CardContent className="pt-10 pb-8 flex flex-col items-center text-center space-y-4">
          <div className="h-16 w-16 bg-primary/10 rounded-full flex items-center justify-center text-primary mb-2">
            <CheckCircle2 size={32} />
          </div>
          <h2 className="text-2xl font-semibold tracking-tight">Application Submitted</h2>
          <p className="text-muted-foreground text-sm max-w-[280px]">
            Your registration request has been successfully submitted to the site manager for review. You will be notified once approved.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-md shadow-lg border-muted/40">
      <CardHeader className="space-y-2">
        <CardTitle className="text-2xl font-semibold tracking-tight">Site Registration</CardTitle>
        <CardDescription>
          Complete this form to request access to the construction site.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
            <FormField
              control={form.control}
              name="full_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Full Name</FormLabel>
                  <FormControl>
                    <Input placeholder="John Doe" className="h-11" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="phone_number"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Phone Number</FormLabel>
                  <FormControl>
                    <Input type="tel" placeholder="+1 (555) 000-0000" className="h-11" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="identity_type"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Role / Visitor Type</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger className="h-11">
                        <SelectValue placeholder="Select your role" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="WORKER">Worker</SelectItem>
                      <SelectItem value="VISITOR">Visitor</SelectItem>
                      <SelectItem value="CONTRACTOR_REPRESENTATIVE">Contractor Representative</SelectItem>
                      <SelectItem value="SITE_ENGINEER">Site Engineer</SelectItem>
                      <SelectItem value="INSPECTOR">Inspector</SelectItem>
                      <SelectItem value="VENDOR">Vendor</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="h-12 w-full text-base font-medium mt-2"
              disabled={registerMutation.isPending}
            >
              {registerMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Submitting...
                </>
              ) : (
                "Submit Request"
              )}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
