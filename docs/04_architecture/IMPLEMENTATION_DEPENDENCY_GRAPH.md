# Implementation Dependency Graph

## Dependency Chains
**Chain A (Backend Core):** EDR-003 -> EDR-001 -> EDR-007
*(Transaction boundaries must be established before moving logic, which in turn simplifies idempotency implementation.)*

**Chain B (Backend Concurrency):** EDR-003 -> [EDR-005, EDR-006]
*(Transaction ownership impacts how locks and concurrency controls are applied.)*

---

## EDR-001: Inconsistent Router Thinness
- **Depends On:** EDR-003
- **Blocks:** EDR-007
- **Can Run In Parallel:** No (Should follow EDR-003)
- **Recommended Order:** 2
- **Implementation Notes:** Ensure transaction boundaries (EDR-003) are stable before relocating logic to the service layer.

## EDR-002: Brittle Database Connection String Parsing
- **Depends On:** None
- **Blocks:** None
- **Can Run In Parallel:** Yes
- **Recommended Order:** N/A (Post-MVP)
- **Implementation Notes:** Deferred to enterprise deployment phase.

## EDR-003: Delegated Transaction Ownership Breaking Atomicity
- **Depends On:** None
- **Blocks:** EDR-001, EDR-005, EDR-006
- **Can Run In Parallel:** No (Foundational)
- **Recommended Order:** 1
- **Implementation Notes:** This is the most critical structural dependency. It must be implemented first to ensure subsequent concurrency and logic refactors have stable boundaries.

## EDR-004: Broken Atomicity in Atomic Sequences
- **Depends On:** None
- **Blocks:** None
- **Can Run In Parallel:** N/A
- **Recommended Order:** N/A (Rejected)
- **Implementation Notes:** No dependency exists.

## EDR-005: Check-Then-Act Race Conditions in Registration
- **Depends On:** EDR-003
- **Blocks:** None
- **Can Run In Parallel:** Yes (with EDR-006)
- **Recommended Order:** 2
- **Implementation Notes:** Requires stable transaction boundaries to implement safe locking or unique constraints.

## EDR-006: Incomplete Optimistic Concurrency Control
- **Depends On:** EDR-003
- **Blocks:** None
- **Can Run In Parallel:** Yes (with EDR-005)
- **Recommended Order:** 2
- **Implementation Notes:** ORM-level concurrency mapping is dependent on correct transaction boundaries.

## EDR-007: Suboptimal Idempotency in Approvals
- **Depends On:** EDR-001
- **Blocks:** None
- **Can Run In Parallel:** No
- **Recommended Order:** 3
- **Implementation Notes:** Wait for the router logic to be moved to the service layer (EDR-001) before implementing idempotency logic.

## EDR-008: Synchronous I/O Blocking for Notifications
- **Depends On:** None
- **Blocks:** None
- **Can Run In Parallel:** N/A
- **Recommended Order:** N/A (Rejected)
- **Implementation Notes:** No dependency exists.

## EDR-009: Ignored Migration Failures at Startup
- **Depends On:** None
- **Blocks:** None
- **Can Run In Parallel:** Yes
- **Recommended Order:** N/A (Post-MVP)
- **Implementation Notes:** Deferred to enterprise deployment phase.

## EDR-010: Leaking Domain Boundaries in State Management
- **Depends On:** None
- **Blocks:** None
- **Can Run In Parallel:** Yes (Independent Frontend Task)
- **Recommended Order:** 1 (Frontend)
- **Implementation Notes:** This is a purely frontend architectural concern and can be executed completely parallel to backend refactoring.
