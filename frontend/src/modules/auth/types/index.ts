export interface User {
  id: string;
  email: string;
  name?: string;
  role: string;
  company_id: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
