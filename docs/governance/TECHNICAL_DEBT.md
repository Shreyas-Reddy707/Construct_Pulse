# ConstructPulse Technical Debt Register

**Document ID:** CP-TD-001  
**Version:** 1.0  
**Status:** Active  
**Owner:** ConstructPulse Engineering  
**Last Updated:** July 2026

---

# Purpose

This document records all approved technical debt within ConstructPulse.

Technical debt is an intentional engineering compromise accepted to support project delivery.

Technical debt must:

- Be documented
- Have a clear reason
- Have an expected resolution
- Never be forgotten

Undocumented technical debt is prohibited.

---

# Status Definitions

| Status | Description |
|----------|-------------|
| Open | Identified but unresolved |
| Planned | Scheduled for implementation |
| In Progress | Currently being addressed |
| Resolved | Fully removed |
| Accepted | Permanent design trade-off |

---

# Priority Definitions

| Priority | Meaning |
|-----------|---------|
| Critical | Security or data integrity risk |
| High | Major architectural impact |
| Medium | Should be resolved before production |
| Low | Minor improvement |

---

# TD-001

## Title

JWT permission_version Placeholder

### Status

Open

### Priority

Medium

### Description

The JWT currently contains a static permission_version value.

The documentation defines the claim but does not define how it should be generated.

### Impact

Authorization

Permission caching

RBAC

### Resolution

Resolve after RBAC Matrix approval and Authorization Engine implementation.

---

# TD-002

## Title

Temporary firebase_uid Placeholder

### Status

Open

### Priority

Medium

### Description

Company Administrators are currently provisioned with a placeholder firebase_uid until Firebase OTP activation is implemented.

### Impact

Authentication

Identity

### Resolution

Replace during Company Administrator Activation.

---

# TD-003

## Title

Authorization Engine Pending

### Status

Planned

### Priority

High

### Description

Authorization Foundation establishes only the RBAC schema.

Runtime permission evaluation has not yet been implemented.

### Impact

Permission enforcement

Endpoint authorization

### Resolution

Sprint 2

Authorization Engine.

---

# TD-004

## Title

RBAC Matrix Pending Approval

### Status

Open

### Priority

High

### Description

Permission Groups and Role assignments remain under architectural review.

Authorization implementation must wait until the RBAC Matrix is approved.

### Impact

Authorization

Permissions

Role mappings

### Resolution

Approve CP-RBAC-001.

---

# TD-005

## Title

Firebase Authentication Integration

### Status

Planned

### Priority

Medium

### Description

Authentication currently supports the foundational identity model.

Firebase OTP integration remains pending.

### Resolution

Company Administrator Activation.

---

# Technical Debt Policy

Technical debt must never be introduced without:

- Documentation
- Justification
- Planned resolution

When resolving technical debt:

- Update this document.
- Reference the implementing ADR or Sprint.
- Mark the debt as Resolved.

---

# TD-006

## Title

Pending Safety Foundation Migration

### Status

Open

### Priority

High

### Description

Safety Foundation models are implemented.
Migration generation is blocked by unresolved PostgreSQL ENUM migration issues from previous batches.

### Resolution

Generate and execute the migration immediately after the migration chain is repaired.

### Impact

Safety Foundation cannot be deployed until migration exists.

---
