import { z } from "zod";

export const loginSchema = z.object({
  phone: z.string().min(10, { message: "Please enter a valid phone number" }),
  otp: z.string().optional(),
});

export type LoginFormValues = z.infer<typeof loginSchema>;

export const registrationSchema = z.object({
  full_name: z.string().min(2, { message: "Full name is required" }),
  phone_number: z.string().min(10, { message: "Please enter a valid phone number" }),
  identity_type: z.enum([
    "WORKER",
    "VISITOR",
    "CONTRACTOR_REPRESENTATIVE",
    "SITE_ENGINEER",
    "INSPECTOR",
    "VENDOR"
  ]),
});

export type RegistrationFormValues = z.infer<typeof registrationSchema>;
