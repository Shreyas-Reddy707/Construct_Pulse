# Implementation Batches

## Batch 1: Core Transaction & Concurrency Integrity

**Purpose:** 
Resolve foundational database interaction flaws that threaten atomicity and data consistency under load.

**Verified EDRs:**
- **EDR-003:** Delegated Transaction Ownership Breaking Atomicity
- **EDR-005:** Check-Then-Act Race Conditions in Registration
- **EDR-006:** Incomplete Optimistic Concurrency Control

**Why grouped together:**
All three EDRs relate to the backend database interaction layer and ORM configuration. Fixing transaction lifecycles (EDR-003) is a prerequisite for robustly handling concurrency controls and race conditions.

**Prerequisites:** None.

**Dependencies:** These issues block safe implementation of complex, multi-service workflows.

**Implementation Risk:** High. Changes to `get_db` and transaction boundaries affect every API endpoint.
**Complexity:** High.
**Business Value:** High (Data Integrity).
**Estimated Size:** Large.

**Expected Deliverables:**
- Centralized Unit-of-Work / transaction boundaries in routers/middleware.
- Unique constraints or explicit locking in `RegistrationService`.
- `version_id_col` mappings on ORM models.

**Suggested Prompt Strategy:**
"Refactor FastAPI database dependency injection to yield transactions per-request. Apply optimistic concurrency `__mapper_args__` to models. Resolve TOCTOU race conditions in `detect_duplicates`."

---

## Batch 2: API Architecture & Reliability

**Purpose:** 
Ensure the backend routing layer is maintainable and resilient to mobile network instabilities.

**Verified EDRs:**
- **EDR-001:** Inconsistent Router Thinness
- **EDR-007:** Suboptimal Idempotency in Approvals

**Why grouped together:**
Both findings involve refactoring the FastAPI router layer. Moving logic into services (EDR-001) will make it much easier to implement and test idempotent state transitions (EDR-007) cleanly.

**Prerequisites:** Batch 1 (Transaction boundaries should be established before refactoring service calls).

**Dependencies:** Unblocks cleaner testing and mobile client retry logic.

**Implementation Risk:** Medium.
**Complexity:** Medium.
**Business Value:** Medium (Reliability & Maintainability).
**Estimated Size:** Medium.

**Expected Deliverables:**
- Business logic extracted from `api/endpoints/users.py` into dedicated services.
- `200 OK` (Idempotent success) returned for repeated valid approval requests.

**Suggested Prompt Strategy:**
"Refactor `users.py` to extract inline logic into the service layer following thin-controller patterns. Update the approval endpoint to act idempotently, returning 200 OK for already-approved requests."

---

## Batch 3: Flutter State Architecture

**Purpose:** 
Decouple frontend feature domains to preserve the Feature-First architecture.

**Verified EDRs:**
- **EDR-010:** Leaking Domain Boundaries in State Management

**Why grouped together:**
Isolated frontend architecture improvement.

**Prerequisites:** None.

**Dependencies:** Unblocks cleaner multi-team mobile development.

**Implementation Risk:** Low.
**Complexity:** Medium.
**Business Value:** Medium (Maintainability).
**Estimated Size:** Small.

**Expected Deliverables:**
- Refactored `attendance_providers.dart` removing cross-domain imports.
- Orchestration or event-driven invalidation for dashboard/occupancy providers.

**Suggested Prompt Strategy:**
"Refactor Riverpod state management in `attendance_providers.dart` to remove direct imports and manipulations of Dashboard and Occupancy providers, utilizing a decoupled state invalidation strategy."

---

## Batch 4: Post-MVP & Rejected (No Immediate Action)

**Purpose:** 
Categorization of verified EDRs that do not require implementation before the MVP release.

**Verified EDRs:**
- **EDR-002:** Brittle Database Connection String Parsing (Post-MVP)
- **EDR-009:** Ignored Migration Failures at Startup (Post-MVP)
- **EDR-004:** Broken Atomicity in Atomic Sequences (Rejected)
- **EDR-008:** Synchronous I/O Blocking for Notifications (Rejected)

**Why grouped together:**
These require zero implementation effort during the current development sprint. EDR-002 and EDR-009 will be addressed when preparing for enterprise deployment. EDR-004 and EDR-008 were incorrect or expected behaviors.

**Prerequisites:** N/A
**Dependencies:** N/A
**Implementation Risk:** None.
**Complexity:** N/A
**Business Value:** N/A
**Estimated Size:** None.

**Expected Deliverables:** None.
**Suggested Prompt Strategy:** N/A
