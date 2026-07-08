# ConstructPulse - Backend Architecture Audit Report

**Date:** July 2026  
**Auditor:** Senior Backend Architect  
**Scope:** `backend/app/` (FastAPI / SQLAlchemy / Python)

This report evaluates the engineering quality and production readiness of the ConstructPulse backend. Findings are based on verified repository evidence.

---

## 1. Overall Architecture

### Observation: Inconsistent Router Thinness
**Evidence:** While `api/endpoints/attendance.py` is perfectly thin (delegating immediately to `AttendanceService`), `api/endpoints/users.py` contains an inline `_update_worker_status` function (150 lines in) that executes complex cross-domain logic, such as automatically checking out active attendance sessions when a worker is suspended.
**Risk:** High coupling. Business logic embedded in the presentation layer prevents reuse, makes unit testing difficult, and breaks the "Thick Services, Thin Controllers" philosophy established elsewhere.
**Recommendation:** Refactor the logic in `users.py` into a dedicated `WorkerService` or `UserService`.
**Priority:** 🟠 High

---

## 2. API Design

### Observation: Domain Exception Bleeding
**Evidence:** `AttendanceService.check_in` throws raw Python `ValueError("ACCESS_DECISION_EXPIRED...")`. The router `attendance.py` uses a blanket `except ValueError as e:` to catch this and return a 400 Bad Request.
**Risk:** Generic `ValueError` catching is dangerous because it could inadvertently swallow unrelated internal errors (e.g., a type casting error inside the service) and expose them directly to the client as 400s instead of 500s.
**Recommendation:** Implement custom domain exception classes (e.g., `DomainException`, `ResourceNotFoundException`) and use FastAPI global exception handlers.
**Priority:** 🟡 Medium

---

## 3. Database Layer & Performance

### Observation: Severe N+1 Query Risks
**Evidence:** 
1. In `api/endpoints/users.py` (`get_user_sites`), the endpoint simply returns `user.assigned_sites`. Since `assigned_sites` is a relationship, this triggers a lazy-load query per request.
2. In `authorization_service.py`, the loop `for group in role.permission_groups:` followed by `for permission in group.permissions:` triggers multiple synchronous DB queries per authentication check.
**Risk:** As traffic scales, these lazy loads will paralyze the database with excessive, repetitive querying.
**Recommendation:** Use SQLAlchemy's `joinedload` or `selectinload` to eager-load relationships when they are known to be serialized in the response.
**Priority:** 🔴 Critical

### Observation: Expensive In-Memory Aggregations
**Evidence:** In `attendance_service.py` (`get_my_today_attendance`), the service fetches all attendance records for the day into Python memory, then loops over them to manually calculate `hours_today += duration`.
**Risk:** Inefficient use of application memory and CPU. 
**Recommendation:** Push mathematical aggregations down to the database using SQLAlchemy's `func.sum()` and `func.extract()`.
**Priority:** 🟠 High

### Observation: Brittle Database Connection String Parsing
**Evidence:** In `db/database.py`, the engine is created with `settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")`.
**Risk:** If the environment variable changes its scheme or uses a different driver prefix, this string replacement will fail silently or break connection initialization.
**Recommendation:** Use Pydantic's `PostgresDsn` for the settings schema to enforce correct URI formatting natively.
**Priority:** 🟢 Low

---

## 4. Security

### Observation: Deprecated Authorization Components Still in Active Use
**Evidence:** `api/deps.py` contains a `RoleChecker` class explicitly marked with `DEPRECATED: Use PermissionChecker instead.` However, `api/endpoints/users.py` still actively relies on it (e.g., `Depends(RoleChecker([UserRole.COMPANY_ADMIN]))`).
**Risk:** Spreading technical debt and creating split-brain authorization patterns where some endpoints check raw roles and others check fine-grained permissions.
**Recommendation:** Migrate all endpoints to `PermissionChecker` and completely remove `RoleChecker`.
**Priority:** 🟠 High

### Observation: Solid Multi-Tenant Isolation
**Evidence:** `api/deps.py` enforces tenant context via `get_current_tenant`, which validates `current_user.company_id` and fetches the tenant record before injecting it into endpoints (e.g., `read_users` in `users.py`).
**Risk:** N/A. This is a positive finding.
**Recommendation:** Maintain this pattern strictly.
**Priority:** 🟢 Low

---

## 5. Production Readiness

### Observation: Lack of Structured Logging
**Evidence:** `users.py` uses standard string interpolation: `logger.info(f"Admin {admin.id} changed user {user_id} status...")`.
**Risk:** Standard string logs are difficult to parse in modern observability stacks (like ELK or Datadog) compared to structured JSON logs.
**Recommendation:** Implement structured JSON logging (e.g., using `structlog` or `python-json-logger`) ensuring `user_id`, `company_id`, and `trace_id` are indexed fields.
**Priority:** 🟡 Medium

### Observation: Pending Authorization Runtime
**Evidence:** Cross-referenced from `TECHNICAL_DEBT.md`. The `PermissionChecker` depends on the `AuthorizationService`, but the underlying RBAC definitions are not finalized.
**Risk:** Production launch cannot occur securely until the RBAC matrix is finalized and tested.
**Recommendation:** Block production release until the RBAC Matrix is approved and tested end-to-end.
**Priority:** 🔴 Critical
