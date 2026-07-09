# ConstructPulse Implementation Workstreams

This document establishes the strategic implementation plan for ConstructPulse. Rather than executing individual, disconnected Engineering Decisions (EDRs), implementation is organized into highly cohesive **Engineering Workstreams**. This approach groups related architectural tasks to minimize merge conflicts, ensure systematic refactoring, reduce regression risk, and maximize development velocity.

---

## Workstream 1: Backend Foundation

**Purpose:** Establish a robust, predictable, and structurally sound backend foundation before executing complex concurrent operations. This workstream stabilizes the core Service Layer and ensures atomic operations across the platform.

**Engineering Decisions Included:**
- **EDR-001:** Service Layer Refactoring (Moving business logic out of API routers).
- **EDR-003:** Transaction Boundaries & Unit of Work (Removing service-level commits).
- **EDR-010:** Architectural Boundary Enforcement (Eliminating cross-domain implicit imports).
- **EDR-021:** Exception Handling Standardization (Replacing opaque `ValueError` swallowing with strongly-typed API exceptions).

**Dependencies:** None. This is the foundational workstream.
**Estimated Complexity:** High. Requires careful refactoring of existing database sessions and service contracts.
**Estimated Business Value:** Critical. Prevents partial database writes and ensures predictable system behavior.
**Estimated Engineering Risk:** High. Modifying transaction boundaries carries the risk of introducing new deadlocks if not tested thoroughly.

**Expected Deliverables:** 
- A standardized `Unit of Work` pattern utilizing FastAPI dependencies.
- Pure service layers devoid of SQLAlchemy `commit()` calls.
- A global exception handler intercepting typed business exceptions.
- Strict enforcement of the Feature-First architectural directory structure.

---

## Workstream 2: Concurrency & Data Integrity

**Purpose:** Protect the platform against race conditions, duplicated data, and concurrent modification collisions—especially critical for high-volume environments like site registration and worker attendance.

**Engineering Decisions Included:**
- **EDR-005:** Database-level constraint enforcement (TOCTOU registration race conditions).
- **EDR-006:** Optimistic Concurrency Control (Implementing SQLAlchemy `version_id_col`).
- **EDR-007:** Idempotent State Transitions (Network retry safety).

**Dependencies:** Workstream 1 (Backend Foundation). Reliable concurrency requires solid transaction boundaries.
**Estimated Complexity:** Medium.
**Estimated Business Value:** High. Prevents severe data corruption and invalid state transitions (e.g., duplicate check-ins).
**Estimated Engineering Risk:** Medium. Adding constraints to existing data models requires careful database migrations.

**Expected Deliverables:**
- Unique constraints applied at the database schema level.
- `version_id` columns implemented on highly-mutated tables (e.g., Attendance, Occupancy).
- Idempotency keys or state-checks applied to critical mutations.

---

## Workstream 3: Authorization & Security

**Purpose:** Consolidate fragmented security implementations into a single, unified enterprise security architecture, eliminating legacy code and ensuring session reliability.

**Engineering Decisions Included:**
- **EDR-022:** RBAC Migration (Removing the legacy `RoleChecker`).
- **EDR-023:** Permission Matrix Finalization (Deploying `PermissionChecker`).
- **EDR-024:** Authentication Session Reliability (Resolving unhandled JWT refresh failures causing zombie sessions).

**Future Improvements (Discovered during verification):**
- **Rate Limiting:** Implementing a functional `slowapi` configuration to protect endpoints from DoS attacks (derived from rejected EDR-032).
- **Dynamic CORS:** Migrating static CORS domains to environment variables (derived from rejected EDR-032).
- **Tenant Isolation Wrapper:** While current manual filtering functions for MVP, future efforts should centralize `company_id` enforcement (derived from rejected EDR-031).

**Dependencies:** Workstream 1 (Backend Foundation).
**Estimated Complexity:** Medium.
**Estimated Business Value:** Critical. Ensures strict data privacy and enterprise compliance.
**Estimated Engineering Risk:** High. Security refactoring can accidentally lock out valid users or expose restricted endpoints.

**Expected Deliverables:**
- Complete removal of `RoleChecker`.
- Comprehensive deployment of `PermissionChecker` across all endpoints.
- Robust frontend token refresh interceptor.

---

## Workstream 4: Performance & Scalability

**Purpose:** Optimize database interactions and network payloads to ensure the platform scales efficiently with increasing enterprise workload.

**Engineering Decisions Included:**
- **EDR-025:** Backend Query Optimization (Eliminating N+1 queries via SQLAlchemy eager loading).
- **EDR-027:** Client-Side Filtering Elimination (Implementing server-side pagination and filtering in Riverpod).

**Dependencies:** Workstream 1 (Backend Foundation) and Workstream 3 (Authorization & Security).
**Estimated Complexity:** Medium.
**Estimated Business Value:** High. Directly impacts perceived application speed and reduces server hosting costs.
**Estimated Engineering Risk:** Low. Query optimizations are highly testable.

**Expected Deliverables:**
- Use of `joinedload` and `selectinload` in complex backend queries.
- Implementation of paginated REST endpoints.
- Flutter providers updated to utilize infinite scrolling and server-side search parameters.

---

## Workstream 5: Flutter Architecture

**Purpose:** Elevate the frontend to enterprise standards by enforcing architectural boundaries, establishing responsive layouts, and improving user interaction feedback.

**Engineering Decisions Included:**
- **EDR-011:** Live UI Refresh (Implementing periodic rebuilds for duration/timer strings).
- **EDR-016:** Responsive Layouts (Establishing adaptive layouts for tablet/iPad experiences).
- **EDR-017:** Material Interaction Feedback (Applying `InkWell` touch ripples globally).

**Future Improvements (Discovered during verification):**
- **Standardized UI States:** Enforcing the usage of `EmptyState` and `ErrorState` components across all feature domains to prevent blank white screens during network failure (derived from rejected EDR-033).

**Dependencies:** Workstream 4 (Performance & Scalability - specifically server-side pagination).
**Estimated Complexity:** High. Layout refactoring affects a large percentage of the UI codebase.
**Estimated Business Value:** High. Tablet optimization is a massive competitive advantage for field workers in construction.
**Estimated Engineering Risk:** Low. UI modifications are visually verifiable and carry low data-loss risk.

**Expected Deliverables:**
- Implementation of a global layout builder for tablet form factors.
- `Timer.periodic` integrations for active worker durations.
- Global application of Material touch feedback.

---

## Workstream 6: Developer Experience & Documentation

**Purpose:** Formalize project onboarding, align configuration management, and ensure the repository is maintainable by future engineering hires.

**Engineering Decisions Included:**
- **EDR-029:** Developer Onboarding Improvements (Documenting Firebase Admin SDK setup).

**Dependencies:** None. Can be executed simultaneously with any workstream.
**Estimated Complexity:** Low.
**Estimated Business Value:** Medium. Reduces engineering onboarding time and prevents configuration errors.
**Estimated Engineering Risk:** None.

**Expected Deliverables:**
- Comprehensive Firebase configuration documentation.
- Updated `.env.example` configurations.

---

## Implementation Order

To minimize merge conflicts and ensure structural dependencies are respected, the workstreams must be executed in the following order:

1. **Workstream 1 (Backend Foundation):** *BLOCKING.* Must execute first. It alters the fundamental way database sessions and services operate.
2. **Workstream 2 (Concurrency) & Workstream 3 (Security):** *PARALLEL.* Once the foundation is stable, database constraints (WS2) and authorization (WS3) can be implemented simultaneously by different backend engineers.
3. **Workstream 4 (Performance):** *SEQUENTIAL.* Optimizing queries and implementing server-side pagination relies on the finalized service layers from WS1 and WS3.
4. **Workstream 5 (Flutter Architecture):** *SEQUENTIAL.* Frontend UI refactoring should begin only after the backend API contracts (pagination, payload structures) are finalized by WS4.
5. **Workstream 6 (Developer Experience):** *PARALLEL.* Documentation and configuration updates can occur concurrently throughout the entire implementation lifecycle.

---

## Overall Engineering Strategy

Executing implementation through organized workstreams is vastly superior to implementing Engineering Decisions sequentially. 

A one-by-one EDR approach results in disjointed code churn, repeated regression testing on the same files, and massive merge conflicts across the team. By contrast, a Workstream-driven strategy isolates changes into specific architectural domains (e.g., all database transaction logic is handled at once; all security logic is handled at once). This reduces context switching, ensures holistic system design, minimizes architectural regression, and dramatically accelerates the velocity at which ConstructPulse can achieve MVP readiness.
