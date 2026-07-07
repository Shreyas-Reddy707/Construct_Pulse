# Backend Startup & Repository Integrity Audit

## 1. Executive Summary
**Overall Startup Health:** **FAIL**

The backend repository is internally inconsistent and cannot successfully start up from a clean clone. The application fails immediately during the import resolution phase due to missing classes, missing enums, and abandoned refactors across the data model and service layers.

---

## 2. Startup Flow Analysis
The expected startup sequence (`uvicorn main:app --reload`) follows this path:
1. `main.py` initialization
2. `app.api.api` import (API Router registration)
3. `app.api.endpoints` imports
4. `app.schemas` imports
5. `app.models` imports

**Failure Points:**
- The process halts at step 4 (`app.schemas.schemas`) before the FastAPI application can even initialize.
- A critical `ImportError` prevents `main.py` from loading successfully because schemas attempt to import non-existent enums from `models.py`. 
- If this first failure is bypassed, subsequent `ImportError`s trigger in `__init__.py`, `payroll_service.py`, and `visitor_service.py`.

---

## 3. Import Audit

| Broken Import | File | Severity | Root Cause |
| --- | --- | --- | --- |
| `CheckInMethod` | `app/schemas/schemas.py` | **Critical** | Enum was renamed (likely to `AttendanceMethod`) or removed from `models.py`, but the import in `schemas.py` was not updated. |
| `OccupancyResponse` | `app/schemas/__init__.py` | **Critical** | Schema was removed from `schemas.py` but is still exported by the package `__init__.py`. |
| `WorkerProfile` | `app/services/payroll_service.py` | **Critical** | Model was removed or renamed in `models.py`, but the service still imports and queries it. |
| `AttendancePunch` | `app/services/visitor_service.py` | **Critical** | Schema was removed from `schemas.py`, but the service still imports and references it. |
| `ComplianceStatus`, `EscortStatus`, `NotificationStatus`, `ApprovalStatus`, `VisitorStatus`, `VisitorType` | `app/schemas/schemas.py` | **High** | These enums were removed from `models.py`. While unused in the schema file itself, they will trigger fatal `ImportError`s once `CheckInMethod` is resolved. |

---

## 4. Model Audit
**Consistency Review:**
- The ORM models (`app/models/models.py`) underwent a significant refactor (likely during Sprint 6), but downstream dependencies were not aligned.
- Several Enums were deleted or consolidated (e.g. `CheckInMethod` → `AttendanceMethod`), creating a mismatch with the schema layer.
- `WorkerProfile` appears to have been merged or removed, breaking existing service logic.

---

## 5. Schema Audit
**Consistency Review:**
- `schemas.py` is out of sync with `models.py`. It requests at least 7 enums that no longer exist.
- The `app/schemas/__init__.py` file contains stale exports (`OccupancyResponse`), preventing the module from loading.
- Missing schemas (`AttendancePunch`) demonstrate that previous features were partially deleted without cleaning up dependent services.

---

## 6. Service Audit
**Consistency Review:**
- `app/services/payroll_service.py` is broken due to a hard dependency on the deleted `WorkerProfile` model.
- `app/services/visitor_service.py` is broken due to a hard dependency on the deleted `AttendancePunch` schema.
- The dependency graph cannot be fully evaluated dynamically because the Python interpreter crashes during the import phase.

---

## 7. API Layer Audit
**Consistency Review:**
- The API router registration (`app/api/api.py`) is intact, but the endpoints cannot be registered because their underlying services and schemas fail to import.
- Dependency injection (e.g., `get_current_user`, `RoleChecker`, `PermissionChecker`) appears structurally correct, but cannot be evaluated at runtime until the core imports are fixed.

---

## 8. Dependency Audit
**Package Analysis:**
- `requirements.txt` specifies `fastapi==0.136.3`, which is an irregular version number (latest FastAPI versions follow `0.115.x` or `0.111.x` depending on the environment cache). This may cause resolution or caching issues on a fresh install depending on the pip index.
- The dependency installation (`pip install -r requirements.txt`) succeeds syntactically, but the environment immediately crashes upon execution due to the source code inconsistencies.

---

## 9. Repository Integrity
- **Stale Code:** `schemas.py` contains unused, broken imports at the top of the file.
- **Abandoned Refactors:** The model layer was refactored without updating `schemas.py`, `payroll_service.py`, or `visitor_service.py`, indicating a partially completed migration.
- **Architectural Inconsistencies:** `__init__.py` files were not kept up to date with the files they export.

---

## 10. Risk Assessment

- **Critical:** 
  - `ImportError` for `CheckInMethod` blocks the entire application startup.
  - `ImportError` for `OccupancyResponse` blocks the schema package initialization.
  - `ImportError` for `WorkerProfile` blocks the payroll endpoints.
  - `ImportError` for `AttendancePunch` blocks the visitor endpoints.
- **High:**
  - Multiple unused and missing enum imports in `schemas.py` that will crash the application as soon as the first critical error is bypassed.
- **Medium/Low:**
  - Unverified `fastapi==0.136.3` version constraint.

---

## 11. Required Fixes
*(Listed in priority order to achieve backend startup)*

1. **Fix Schema Enums:** Remove the missing enum imports (`CheckInMethod`, `ComplianceStatus`, `EscortStatus`, `NotificationStatus`, `ApprovalStatus`, `VisitorStatus`, `VisitorType`) from `app/schemas/schemas.py`. Map any usages to their modern equivalents (e.g., `AttendanceMethod`).
2. **Fix Schema Exports:** Remove `OccupancyResponse` from `app/schemas/__init__.py`.
3. **Fix Payroll Service:** Update `app/services/payroll_service.py` to remove the import of `WorkerProfile` and replace the logic that queries it with the current model (e.g., `User` or a new profile table).
4. **Fix Visitor Service:** Update `app/services/visitor_service.py` to remove the import of `AttendancePunch` and replace it with the modern schema equivalent.

---

## 12. Certification

**FAIL**

**Justification:** A fresh clone of the repository cannot start successfully. The backend is non-functional out-of-the-box due to multiple fatal `ImportError` exceptions stemming from an incomplete refactor of the models and schemas. A developer cannot run `uvicorn main:app --reload` without first modifying the repository code to fix these broken references.
