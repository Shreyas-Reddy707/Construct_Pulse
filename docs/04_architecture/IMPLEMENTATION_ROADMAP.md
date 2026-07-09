# Implementation Roadmap

## Purpose
This document serves as the executive engineering roadmap for ConstructPulse. It outlines the execution strategy for addressing verified engineering decisions (EDRs). This roadmap ensures that foundational architecture, concurrency, and reliability issues are resolved before MVP, while appropriately deferring lower-risk or future-state items.

## Current Verification Summary
At the time of this roadmap's creation, the following 10 Engineering Decisions (EDR-001 through EDR-010) have been verified:
- **Verified EDRs:** 10
- **Total EDRs:** 33

## Decision Statistics (Verified Sub-set)
- **Improve Before MVP:** 6 (EDR-001, EDR-003, EDR-005, EDR-006, EDR-007, EDR-010)
- **Post-MVP:** 2 (EDR-002, EDR-009)
- **Rejected:** 2 (EDR-004, EDR-008)

## Engineering Philosophy
1. **Foundation First:** Core architectural integrity, data consistency, and safe state management must be established before building outward.
2. **Defensible Postponement:** If a finding does not pose an immediate risk to MVP functionality or state integrity, it is deferred to post-MVP to preserve engineering velocity.
3. **Data Integrity is Non-Negotiable:** Missing transaction atomicity and race conditions are high-priority structural risks that must be fixed.

## Guiding Principles
- **No Feature Work During Foundation Phases:** Feature development must be paused while core transaction management and state management architectures are refactored.
- **Fail Fast (Post-MVP):** The system should crash if its external dependencies (like migrations) are unfulfilled, although this is deferred to enterprise scale.
- **Strict Boundary Enforcement:** Clean Architecture and Feature-First design must be enforced to prevent spaghetti dependencies.

## Implementation Phases

### Phase 1: Core Transaction & Concurrency Integrity
**Priority:** Highest
**Goals:** Secure the backend database interaction model. Ensure atomicity of complex operations and prevent data corruption from concurrent requests.
**Business Value:** Prevents silent data corruption, lost updates, and duplicate registrations, ensuring a reliable system of record.
**Estimated Implementation Order:** 1

### Phase 2: API Architecture & Reliability
**Priority:** High
**Goals:** Refactor backend routers for thinness and enforce idempotency on state transitions.
**Business Value:** Enhances the reliability of mobile clients under poor network conditions and significantly improves backend maintainability.
**Estimated Implementation Order:** 2

### Phase 3: Flutter State Architecture
**Priority:** High
**Goals:** Decouple feature domains in the Flutter application.
**Business Value:** Prevents architectural decay on the frontend, enabling faster and safer iteration of new mobile features.
**Estimated Implementation Order:** 3

### Phase 4: Deferred (Post-MVP)
**Priority:** Low
**Goals:** Address deployment, infrastructural, and enterprise-grade readiness checks.
**Business Value:** Enhances deployment robustness and portability for scale.
**Estimated Implementation Order:** 4 (Post-MVP)

## Success Criteria
- Backend transactions reliably commit or rollback as a single unit of work.
- Parallel concurrent requests cannot bypass registration uniqueness checks.
- Optimistic concurrency control is actively enforced by the ORM.
- Flutter features manage their own state without direct cross-domain imports.

## Exit Criteria
- All "Improve Before MVP" tasks are implemented, code-reviewed, and merged.
- End-to-end tests confirm that idempotency and concurrency protections function as designed.
- Architecture tests confirm no cross-domain boundary violations exist in the mobile codebase.
