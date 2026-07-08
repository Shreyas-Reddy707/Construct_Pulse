# ConstructPulse Engineering Decision Register (EDR)

This document is the master engineering register consolidating findings from the Repository Mapping, Documentation Verification, Backend Architecture, Backend Production Engineering, Flutter Architecture, and Flutter UI Engineering audits.

---

## Backend Architecture

### EDR-001: Inconsistent Router Thinness
- **Category:** Backend Architecture
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** `api/endpoints/users.py` contains 150+ lines of inline cross-domain business logic, breaking the "Thin Controllers" pattern.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-002: Brittle Database Connection String Parsing
- **Category:** Backend Architecture
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** Database engine initialization relies on `.replace("postgresql://", "postgresql+psycopg://")` which will fail silently if the DSN format changes.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

---

## Backend Production Engineering

### EDR-003: Delegated Transaction Ownership Breaking Atomicity
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `get_db` delegates `commit()` to individual services, meaning API endpoints composing multiple services suffer from partial commit failures.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-004: Broken Atomicity in Atomic Sequences
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `registration_seq` is consumed before database insertion, meaning a failed insert permanently loses the sequence number.
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

### EDR-005: Check-Then-Act Race Conditions in Registration
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Registration lacks a database `UniqueConstraint` for phone/status, allowing concurrent POST requests to duplicate registrations.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-006: Incomplete Optimistic Concurrency Control
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** The `Attendance` model defines an `attendance_version` column but fails to wire it to SQLAlchemy's `version_id_col`, silently permitting concurrent overwrites.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-007: Suboptimal Idempotency in Approvals
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `ApprovalService` locks rows correctly but throws a 400 error on duplicate concurrent retries instead of returning a 200 OK idempotent response.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

### EDR-008: Synchronous I/O Blocking for Notifications
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `NotificationService` loops thousands of inserts synchronously in the FastAPI thread, risking 504 Gateway Timeouts.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-009: Ignored Migration Failures at Startup
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Application boot silently catches generic `OperationalError` to skip seeding, which masks legitimate database connection outages as mere "missing tables".
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

---

## Flutter Architecture

### EDR-010: Leaking Domain Boundaries in State Management
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** `attendance_providers.dart` tightly couples domains by explicitly importing and mutating dashboard/occupancy state, violating Clean Architecture.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-011: Improper Async State Handling for Live Data
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture & UI Engineering Audits
- **Audit Summary:** Live attendance durations evaluate `DateTime.now()` directly in the build method without a stream/ticker, causing stagnant UI strings.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-012: Complete Absence of Code Generation (False Retrofit Migration)
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit & Documentation Verification
- **Audit Summary:** Despite claims of a Retrofit 10 & Freezed migration, core repositories use raw, error-prone `Dio` and manual `.fromJson()` methods with zero `.g.dart` generated files.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-013: Fragile Path-Based GoRouter Navigation
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** Routing relies entirely on hardcoded string paths rather than typed Route names or enums, increasing runtime crash risks.
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

---

## UI Engineering

### EDR-014: Hardcoded Colors Breaking Material 3 Theming
- **Category:** UI Engineering
- **Source Audit:** Flutter Architecture & UI Engineering Audits
- **Audit Summary:** Widgets manually check brightness and explicitly reference `AppColors.surface` instead of natively hooking into `Theme.of(context).colorScheme`.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-015: Typography Configuration Breaking Dark Mode
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** `AppTypography` statically binds `AppColors.textPrimary` to GoogleFonts generators, forcing text to remain dark and illegible in Dark Mode.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-016: Rigid 2D Layouts Lacking Responsiveness
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Dashboards utilize strict `Row` with `Expanded` columns, causing significant stretching on tablets and squishing on small phones.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-017: Missing Interaction Feedbacks
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Critical UI cards use `GestureDetector` instead of `InkWell`, omitting visual press/ripple feedback and breaking enterprise responsiveness standards.
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

### EDR-018: "Fake" Static Loading Skeletons
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** `ShimmerBox` lacks an animation controller, rendering a static grey rectangle that fails to convey loading activity.
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

### EDR-019: Missing Semantic Accessibility Wrappers
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Forms rely on separate `Text` widgets for labels above input fields without binding them via `Semantics`, degrading screen reader utility.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-020: Massive Inline Widget Sprawl
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering & Flutter Architecture Audits
- **Audit Summary:** Lists build complex 60+ line cards inline rather than extracting components, resulting in duplicated code and inconsistent border/padding designs.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

---

## Security

### EDR-021: Opaque Exception Handling & Domain Bleeding
- **Category:** Security
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** Downstream `ValueError` exceptions are caught uniformly by the router and converted to 400 Bad Requests, destroying stack traces and leaking validation states.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-022: Deprecated Authorization Components Still Active
- **Category:** Security
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** `RoleChecker` is marked deprecated but remains actively utilized by critical endpoints instead of the intended `PermissionChecker`.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-023: Pending Authorization Runtime (RBAC Incomplete)
- **Category:** Security
- **Source Audit:** Backend Architecture Audit & Documentation Verification
- **Audit Summary:** The primary permissions engine is blocked by an unfinalized RBAC matrix, leaving the system functionally insecure for production.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-024: Authentication Interceptor Swallow
- **Category:** Security
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** A failed JWT refresh clears secure storage but does not redirect the GoRouter, stranding users on a dead screen with silent 401s.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

---

## Performance

### EDR-025: Severe N+1 Database Query Risks
- **Category:** Performance
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** The API serializes lazy-loaded relationships (e.g., `user.assigned_sites`) and loops authorization definitions without utilizing `joinedload`.
- **Priority:** 🔴 Critical
- **Current Status:** 🟦 New

### EDR-026: Expensive In-Memory Backend Aggregations
- **Category:** Performance
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** Python manually loops over all daily attendance records to sum durations rather than utilizing PostgreSQL `func.sum()`.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-027: Inefficient Client-Side Data Filtering
- **Category:** Performance
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** The mobile app downloads an entire worker's attendance history just to filter for "today" in Dart memory.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

---

## Documentation

### EDR-028: Missing Offline & Passive Geofencing Capabilities
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** TRD demands offline resilience and background geofencing, but the current app relies strictly on online API requests and manual QR scanning.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-029: Firebase Authentication Flow Discrepancy
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** Architecture docs claim Firebase OTP is active, but implementation relies on placeholders (verified in technical debt).
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

### EDR-030: Missing Asset & Fleet Modules
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** API specs define extensive endpoints for assets/machinery that do not exist in the codebase.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

---

## Future Improvements

### EDR-031: Solid Multi-Tenant Isolation
- **Category:** Future Improvements
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** Excellent dependency injection via `get_current_tenant` guarantees data isolation across companies. Maintain this pattern.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

### EDR-032: Robust Security & Rate-Limiting Configuration
- **Category:** Future Improvements
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Modern implementations of CORS arrays and `slowapi` rate-limiting are properly wired to the environment configuration.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

### EDR-033: Standardized Fallback UI Components
- **Category:** Future Improvements
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Well-designed `EmptyState` and `ErrorState` components ensure the enterprise app avoids blank white screens during network instability.
- **Priority:** 🟢 Low
- **Current Status:** 🟦 New

---

## EDR Summary Statistics

- **Total Findings:** 33
- **Critical Findings:** 10
- **High Findings:** 11
- **Medium Findings:** 6
- **Low Findings:** 6
