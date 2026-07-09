export class ApiError extends Error {
  public readonly status: number;
  public readonly details: unknown;
  public readonly raw: unknown;

  constructor(message: string, status: number, details?: unknown, raw?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
    this.raw = raw;
    
    // Set the prototype explicitly when extending Error in TS
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}
