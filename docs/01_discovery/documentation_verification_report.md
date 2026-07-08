# ConstructPulse - Documentation Verification Report

This report cross-references the official ConstructPulse documentation against the verified implementation chains and deep repository mapping. Its purpose is to establish a verified single source of truth before architecture auditing begins.

---

## 1. SYSTEM ARCHITECTURE.md

**Status:** Partially Outdated / Ahead of Implementation
**Confidence Level:** High

### Discrepancy 1: Authentication Flow
- **Section:** 10. Authentication Architecture (Firebase OTP -> Backend Verification)
- **Evidence:** `SYSTEM ARCHITECTURE.md` claims Firebase Phone Authentication and OTP is the active flow.
- **Actual Implementation:** The flow is not fully wired for all users. As explicitly documented in `docs/governance/TECHNICAL_DEBT.md` (TD-002, TD-005), Firebase Authentication integration remains pending, and Company Administrators are currently provisioned with a placeholder `firebase_uid`.
- **Missing Information Source:** `TECHNICAL_DEBT.md` provides the accurate state of authentication.

### Discrepancy 2: Authorization Engine
- **Section:** 11. Authorization Architecture (RBAC)
- **Evidence:** Claims permissions are enforced at the API and UI level.
- **Actual Implementation:** While the models (`User`, `Role`) and basic schemas exist, the runtime permission evaluation engine is not implemented. `TECHNICAL_DEBT.md` (TD-003, TD-004) confirms the Authorization Engine is pending and the RBAC matrix is not yet approved.

---

## 2. API SPECIFICATION.md & OPENAPI SWAGGER SPEC.md

**Status:** Ahead of Implementation / Partially Conflicts with Implementation
**Confidence Level:** High

### Discrepancy 1: Asset & Fleet Management
- **Section:** Assets, Equipment & Fleet Domain APIs
- **Evidence:** The API specification documents extensive endpoints for managing heavy machinery, vehicles, and temporary facilities (e.g., lines 3636+).
- **Actual Implementation:** There is no `assets.py` router in `backend/app/api/endpoints/`, nor are there corresponding SQLAlchemy models in `models.py`. The feature does not exist in the codebase yet.

### Discrepancy 2: Deprecated Endpoints
- **Section:** Deprecation Policies
- **Evidence:** The documentation marks several legacy endpoints as deprecated.
- **Actual Implementation:** The `backend/app/api/endpoints/auth.py` router retains a legacy `@router.post("/register", deprecated=True)` endpoint. The implementation accurately uses FastAPI's `deprecated=True` flag, meaning the code aligns with the doc's intent, but the documentation implies deprecated endpoints might be removed soon, while they still actively exist in the router.

---

## 3. DATABASE DESIGN md.md

**Status:** Ahead of Implementation
**Confidence Level:** High

### Discrepancy 1: Asset & Fleet Models
- **Section:** Assets, Equipment & Fleet Domain
- **Evidence:** The database design outlines schema requirements for temporary site assets, machinery, and fleet management.
- **Actual Implementation:** A review of `backend/app/models/models.py` reveals no tables for `assets`, `equipment`, or `fleet`. The database schema is currently limited to core identity, attendance, sites, safety, and initial payroll/planning stubs.

---

## 4. FRONTEND IMPLEMENTATION.md & MASTER IMPLEMENTATION.md

**Status:** Partially Outdated
**Confidence Level:** High

### Discrepancy 1: Dependency Ecosystem Versions
- **Section:** Frontend Technology Stack / State Management
- **Evidence:** These master documents describe the architectural use of Riverpod, Freezed, and Retrofit.
- **Actual Implementation:** The repository underwent a recent modernization sprint upgrading to **Riverpod 3**, **Retrofit 10**, and the **Freezed 3.x** ecosystem. The documentation does not reflect these major version bumps, which carry significant API changes (especially Riverpod 3 and Freezed 3).

### Discrepancy 2: Feature Completeness
- **Section:** Module Implementations (Emergency, Reports, Payroll)
- **Evidence:** The documentation describes full flows for these modules.
- **Actual Implementation:** The `feature_implementation_chain.md` proves that while backend models exist, the Flutter application is missing Repositories and Providers for Payroll, Planning, and Reports. Emergency Muster only has UI shells without complete provider wiring.

---

## 5. docs/governance/TECHNICAL_DEBT.md

**Status:** Accurate
**Confidence Level:** Very High

### Verification
- **Section:** All listed debts (TD-001 through TD-006).
- **Evidence:** The document accurately reflects the current state of the codebase.
- **Actual Implementation:** 
  - TD-001 (JWT placeholder) matches the static implementation in `security.py`.
  - TD-002/005 (Firebase pending) matches the lack of frontend Firebase OTP wiring.
  - TD-006 (Safety Migration Blocked) accurately explains why `SafetyObservation` and `Incident` models exist in Python but might lack corresponding active DB tables if the Alembic migration hasn't run.

---

## 6. Technical Requirements Document (TRD)

**Status:** Ahead of Implementation
**Confidence Level:** High

### Discrepancy 1: Offline Capability
- **Section:** System Resilience / Offline Mode
- **Evidence:** Mandates that the application must continue functioning during temporary network loss.
- **Actual Implementation:** The Flutter application's core data layers rely entirely on standard API Clients (Dio). There is no local embedded database (e.g., Isar, SQLite, or Hive) wired into the repositories for offline queuing or sync resolution.

### Discrepancy 2: Passive Geofencing
- **Section:** Operations / Check-ins
- **Evidence:** Mentions passive geofenced check-ins.
- **Actual Implementation:** Check-ins are currently explicitly triggered via QR scans that validate GPS coordinates at the moment of the scan (`AttendanceCheckIn` schema), rather than passive background OS-level geofencing.

---

## Conclusion of Verification

The single source of truth for the *current* state of the repository is the **source code** combined with **`TECHNICAL_DEBT.md`**. 

The majority of the architectural and requirements documentation (`TRD`, `API SPECIFICATION`, `DATABASE DESIGN`) represents the **target end-state** of the platform rather than the current Phase 2 / Sprint 4 reality. Architecture audits moving forward must evaluate the codebase against its own reality rather than assuming all documented requirements have been built.
