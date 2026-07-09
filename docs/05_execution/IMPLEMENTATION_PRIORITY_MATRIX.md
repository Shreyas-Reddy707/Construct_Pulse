# ConstructPulse Implementation Priority Matrix

This document establishes the execution priority for all verified Engineering Decisions (EDRs) and their associated implementation workstreams. 

---

## Priority Philosophy

Implementation priority within ConstructPulse is driven exclusively by engineering risk and architectural dependency, rather than chronological EDR numbering or perceived feature importance. 

Attempting to resolve frontend UI defects before stabilizing backend database transaction boundaries introduces severe regression risks. Therefore, this matrix enforces a strict structural sequence: stabilizing the foundational data and authorization layers before optimizing performance and polishing the presentation layers.

---

## Priority Matrix

### Tier 1: Critical Priority

Items that must be completed before any other implementation can commence. These are structural blockers.

**Workstream 1: Backend Foundation**
- **Engineering Decisions:** EDR-001 (Service Layer Refactoring), EDR-003 (Transaction Boundaries), EDR-010 (Architectural Boundary Enforcement), EDR-021 (Exception Handling).
- **Reason:** Database transaction commits currently exist at the router and service layers, violating the Unit of Work pattern. Any new feature development or bug fixing built on top of this flawed foundation will inherit severe data corruption risks during concurrent requests.
- **Blocking Dependencies:** None.
- **Expected Outcome:** A predictable, atomic, and safe backend service layer capable of handling concurrent mutations without partial writes.

---

### Tier 2: High Priority

Items that should immediately follow Tier 1. These items secure the platform and ensure data integrity under load.

**Workstream 3: Authorization & Security**
- **Engineering Decisions:** EDR-022 (RBAC Migration), EDR-023 (Permission Matrix Finalization), EDR-024 (Session Reliability), Rate Limiting & Dynamic CORS Implementation (Identified in EDR-032).
- **Reason:** Enterprise software cannot deploy to production without functional rate-limiting and a unified RBAC implementation. Legacy `RoleChecker` logic must be excised to prevent unauthorized access.
- **Blocking Dependencies:** Blocked by Tier 1 (Backend Foundation).
- **Expected Outcome:** A secure API protected against DoS attacks, unauthorized access, and cross-tenant data leakage.

**Workstream 2: Concurrency & Data Integrity**
- **Engineering Decisions:** EDR-005 (TOCTOU Registration Fixes), EDR-006 (Optimistic Concurrency), EDR-007 (Idempotent State Transitions).
- **Reason:** As the user base grows, concurrent requests will inevitably collide. Relying on application-level checks without database-level constraints invites duplicate records and corrupted states.
- **Blocking Dependencies:** Blocked by Tier 1 (Backend Foundation).
- **Expected Outcome:** Guaranteed database integrity regardless of network retries or simultaneous API requests.

---

### Tier 3: Medium Priority

Items critical for MVP quality and scale, but which are not strict architectural blockers for other engineers.

**Workstream 4: Performance & Scalability**
- **Engineering Decisions:** EDR-025 (Eliminating N+1 Queries), EDR-027 (Eliminating Client-Side Filtering).
- **Reason:** While the application currently functions, downloading entire datasets to the client and triggering N+1 database queries will cause severe performance degradation at launch. 
- **Blocking Dependencies:** Blocked by Tier 1 (Backend Foundation) and Tier 2 (Authorization). Server-side pagination must be built on secure, transactionally-safe service layers.
- **Expected Outcome:** Fast backend response times, minimal database load, and significantly reduced mobile payload sizes.

---

### Tier 4: Low Priority

Items deferred until remaining MVP structural work is stable. These involve UX polish, layout responsiveness, and developer tooling.

**Workstream 5: Flutter Architecture**
- **Engineering Decisions:** EDR-011 (Live UI Refresh), EDR-016 (Responsive Tablet Layouts), EDR-017 (Material Touch Feedback), Standardized UI Fallbacks (Identified in EDR-033).
- **Reason:** UX improvements provide immense business value but carry low technical risk. They should only be implemented once the backend API contracts (such as server-side pagination from Tier 3) are finalized.
- **Blocking Dependencies:** Blocked by Tier 3 (Performance & Scalability).
- **Expected Outcome:** An enterprise-grade, responsive mobile experience.

**Workstream 6: Developer Experience & Documentation**
- **Engineering Decisions:** EDR-029 (Developer Onboarding Improvements).
- **Reason:** Administrative improvements that do not impact application functionality.
- **Blocking Dependencies:** None (Independent).
- **Expected Outcome:** Streamlined developer onboarding.

---

## Risk vs Business Value Matrix

| Workstream | Engineering Risk | Business Value | Category |
|------------|------------------|----------------|----------|
| **WS1: Backend Foundation** | High | Critical | **High Risk / Critical Value** |
| **WS2: Concurrency & Integrity**| Medium | High | **Medium Risk / High Value** |
| **WS3: Authorization & Security** | High | Critical | **High Risk / Critical Value** |
| **WS4: Performance & Scalability**| Low | High | **Low Risk / High Value** |
| **WS5: Flutter Architecture** | Low | Medium | **Low Risk / Medium Value** |
| **WS6: Developer Experience** | None | Low | **No Risk / Low Value** |

---

## Implementation Sequencing

To maximize development velocity, execution should be sequenced as follows:

1. **Sequential Work:** Workstream 1 (Backend Foundation) must be executed in isolation. All other backend work must wait.
2. **Parallel Work:** Once WS1 is complete, Workstream 2 (Concurrency) and Workstream 3 (Security) can be developed in parallel by separate backend engineers.
3. **Blocked Work:** Workstream 4 (Performance) is blocked until WS1, WS2, and WS3 are integrated. Workstream 5 (Flutter Architecture) is blocked until WS4 finalizes API response payloads.
4. **Independent Work:** Workstream 6 (Developer Experience) can be executed at any time.

---

## Engineering Capacity Recommendation

To execute this matrix efficiently, multiple engineers can safely divide the work without causing severe merge conflicts, provided they respect the sequencing above.

**Phase 1 (Foundation):**
- **Engineer A (Lead Backend):** Executes WS1 (Backend Foundation). Modifies base repository classes and session managers.
- **Engineer B (Backend/Security):** Prepares documentation (WS6) and plans RBAC migration strategy (WS3 prep).
- **Engineer C (Frontend):** Paused on feature development. Focuses on technical debt cleanup not dependent on API changes.

**Phase 2 (Parallel Execution):**
- **Engineer A:** Executes WS2 (Concurrency & Data Integrity). Implements database migrations and constraints.
- **Engineer B:** Executes WS3 (Authorization & Security). Replaces `RoleChecker` and implements rate-limiting.
- **Engineer C:** Executes isolated UI updates for WS5 (Tablet Layouts, Touch Feedback) that do not require API changes.

**Phase 3 (Performance & Finalization):**
- **Engineer A & B:** Collaborate on WS4 (Performance). Optimizing queries and building paginated endpoints.
- **Engineer C:** Completes WS5 (Flutter Architecture) by integrating the new paginated API endpoints into Riverpod.

---

## Executive Recommendation

The recommended strategy is to abandon ad-hoc, ticket-by-ticket engineering execution. 

Prioritizing implementation via this Engineering Matrix is vastly superior to implementing individual EDRs because it acknowledges the physical reality of software architecture. Fixing a frontend bug (e.g., client-side filtering) is pointless if the backend data access layer is fundamentally broken. By enforcing strict architectural dependency sequencing, ConstructPulse will minimize regression defects, avoid duplicated effort, and achieve a stable MVP significantly faster.
