# Backend ↔ Flutter Contract Audit

## 1. Executive Summary
**Overall Contract Health:** **FAIL**

The integration contract between the FastAPI backend and the Flutter mobile application contains critical discrepancies. While standard CRUD patterns and global error handling are highly consistent, the API fails to provide fundamental mobile requirements such as refresh token workflows and multipart file uploads. Furthermore, the dashboard and enum contracts are broken. Flutter development cannot proceed safely until these API contracts are aligned.

---

## 2. Authentication Contract
**Status:** **Contract Mismatch**
- **Login Flow:** The backend `POST /login` consumes a Firebase token and returns a JWT `access_token`. This is implemented.
- **Refresh Flow:** **CRITICAL GAP.** The Flutter client's `AuthInterceptor` is hardcoded to call `POST /api/v1/auth/refresh` using a `refresh_token` upon receiving a 401 response. However, the backend does not return a `refresh_token` during login, nor does it implement the `/refresh` endpoint. 
- **Token Lifetime:** Handled via JWT expiration, but session continuity on mobile will fail due to the missing refresh implementation.

---

## 3. API Contract
**Status:** **Consistent but Lacking Metadata**
- **REST Consistency:** High. Standard GET/POST/PUT/DELETE methods are utilized correctly.
- **Pagination Consistency:** Endpoints (e.g., `users.py`, `sites.py`) use standard `skip` and `limit` query parameters. 
- **Pagination Payload:** **GAP.** List endpoints return raw JSON arrays (`List[Model]`) instead of wrapped paginated objects (e.g., `{ "data": [...], "total": X }`). This prevents Flutter from accurately rendering infinite scrolling limits without fetching until an empty array is returned.

---

## 4. DTO Contract
**Status:** **Rigid Server-Side IDs**
- **Serialization:** Consistent use of standard JSON types and Pydantic validation.
- **UUID Usage:** UUIDs are utilized heavily as primary keys.
- **Client Generation:** **GAP.** DTOs (e.g., `IncidentCreate`) do not accept an `id` field from the client. The backend mandates server-side ID generation, which severely hinders the mobile app's ability to create related entities offline and sync them later.

---

## 5. Enum Contract
**Status:** **Broken**
- **Consistency:** The backend models utilize a robust set of String Enums.
- **Contract Violation:** The `app/schemas/schemas.py` file exposes DTOs relying on missing enums (`CheckInMethod`, `VisitorStatus`, etc.) that were removed from the database models. This renders the OpenAPI schema generation invalid.

---

## 6. Dashboard Contract
**Status:** **Broken Pattern**
- **Expected Pattern:** `report_id`, `generated_at`, `summary`.
- **Actual Implementation:** The `GET /summary` endpoint in `dashboard.py` returns a flat dictionary (`{"total_workers": X, "pending_workers": Y}`). It completely violates the expected structured analytics contract.

---

## 7. Error Handling Contract
**Status:** **Excellent**
- **Implementation:** Global exception handlers in `app.core.exceptions` intercept 400, 404, 422, and 500 errors.
- **Contract:** Errors are uniformly wrapped in a predictable JSON structure: `{"error": {"code": 404, "message": "...", "details": [...]}}`. Flutter can easily build a unified interceptor for this payload.

---

## 8. QR Workflow Contract
**Status:** **Supported**
- **Implementation:** The backend provides dedicated endpoints for `generate-qr`, `refresh-qr`, and `qr` fetching within `sites.py`.
- **Validation:** Attendance endpoints accept `qr_token` payloads, confirming that the backend fully supports site-based QR muster and attendance flows.

---

## 9. Permission Contract
**Status:** **Implicit / Opaque**
- **Backend Implementation:** Routes use explicit string checks like `PermissionChecker("attendance.view")`.
- **Flutter Contract:** The backend JWT payload only injects `role_id` and `permission_version`. The `/me` endpoint only returns the `UserRole`. 
- **Impact:** The backend does not expose a raw array of permissions to the frontend. Flutter lacks the necessary payload to implement dynamic, fine-grained UI hiding based on permissions; it must instead rely on hardcoded Role mappings.

---

## 10. Feature Coverage Matrix

| Feature | Backend | Flutter | Contract Status |
| :--- | :--- | :--- | :--- |
| **Authentication** | Ready | Ready | **Mismatch (Refresh Token)** |
| **Attendance** | Ready | Ready | Ready |
| **Occupancy** | Ready | Ready | Ready |
| **Dashboard** | Ready | Ready | **Mismatch (Structure)** |
| **Emergency Muster** | Ready | Ready | Ready |
| **Notifications** | Ready | Partial | Backend Ready |
| **Payroll** | Ready | Partial | Backend Ready |
| **Planning** | Ready | Partial | Backend Ready |
| **Reporting** | Ready | Partial | Backend Ready |
| **Visitors** | Ready | Missing | Backend Ready |
| **Incidents** | Ready | Missing | Backend Ready |
| **Safety Operations** | Ready | Missing | Backend Ready |
| **Platform Configuration** | Ready | Missing | Backend Ready |

---

## 11. Offline Readiness Audit
**Status:** **Poor**
- **Caching & Sync:** Endpoints do not support `updated_after` timestamp filtering, preventing efficient delta-sync pulls.
- **Offline Queues:** True offline queues require client-generated UUIDs (to map local relationships before syncing). The API contract rejects client-provided IDs on `POST` requests, making robust offline mutation sync highly complex.

---

## 12. File Upload Audit
**Status:** **Missing entirely**
- **Implementation:** There is absolutely no usage of `UploadFile` or multipart form data endpoints in the backend repository.
- **Impact:** The mobile application cannot upload evidence, profile pictures, or report attachments.

---

## 13. Mobile Readiness
**Not Ready.** The backend contracts are currently hostile to mobile consumption. The lack of a refresh token mechanism will force users to repeatedly log in. The lack of file upload support prevents standard incident reporting features. The lack of offline sync primitives will result in a fragile mobile experience in low-connectivity construction sites.

---

## 14. Risk Assessment
- **Critical:** Missing Refresh Token endpoint and payload (breaks mobile sessions).
- **Critical:** Missing File Upload API contract (breaks incident/safety features).
- **High:** Server-generated UUIDs on `POST` (breaks offline queues).
- **High:** Flat dashboard response structure.
- **High:** Missing Enums in OpenAPI generation.

---

## 15. Certification

**FAIL**

**Justification:** The API contract is not viable for Flutter mobile development. While the core CRUD logic and error handling are solid, the absence of mobile-first API necessities (refresh tokens, multipart file uploads, offline sync timestamps, and client-generated IDs) means the frontend engineering team will immediately be blocked upon implementation. The backend requires targeted enhancements before the contract can be certified.

---

**Audit Integrity Confirmation**
- Source files modified: 0
- Source files created: 0
- Source files deleted: 0
- Documentation files created: 1 (`BACKEND_FLUTTER_CONTRACT_AUDIT.md`)
- Repository code changed: No
