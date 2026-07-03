# ConstructPulse Architecture Decision Records (ADR)

**Document ID:** CP-ADR-001  
**Version:** 1.0  
**Status:** Approved  
**Owner:** ConstructPulse Engineering  
**Last Updated:** July 2026

---

# Purpose

This document records significant architectural decisions made during the development of ConstructPulse.

Each Architecture Decision Record (ADR) documents:

- The problem
- The decision
- The rationale
- The consequences

Future architectural changes should reference these ADRs rather than replacing them.

---

# ADR-001

## Title

Documentation-First Development

### Status

Accepted

### Decision

Documentation is the authoritative source of truth for ConstructPulse.

Implementation follows documentation.

Documentation never follows implementation.

### Rationale

Enterprise software requires consistency across developers and AI-assisted implementation.

### Consequences

- Documentation reviewed before coding
- Architecture approved before implementation
- Documentation updated before architectural changes

---

# ADR-002

## Title

Audit Before Implementation

### Status

Accepted

### Decision

Every implementation begins with an architectural audit.

### Rationale

Prevent incorrect implementation and unnecessary refactoring.

### Consequences

Implementation proceeds only after scope and dependencies are understood.

---

# ADR-003

## Title

Schema Before Behaviour

### Status

Accepted

### Decision

Development follows this order:

Schema

↓

Reference Data

↓

Business Behaviour

↓

User Interface

### Rationale

Stable schemas reduce rework and simplify implementation.

### Consequences

Business logic is never implemented before its data model exists.

---

# ADR-004

## Title

Organization Bootstrap Transaction

### Status

Accepted

### Decision

Company creation is an atomic transaction.

The following entities are created together:

- Company
- Company Administrator
- Default Department

### Rationale

Prevent partially provisioned tenants.

### Consequences

Failure in any step rolls back the entire transaction.

---

# ADR-005

## Title

Tenant Isolation

### Status

Accepted

### Decision

Every authenticated request executes within a tenant context.

The tenant is resolved using get_current_tenant().

### Rationale

Guarantees company data isolation.

### Consequences

Repositories always filter using tenant context.

---

# ADR-006

## Title

Company Context Resolution

### Status

Accepted

### Decision

get_current_tenant() returns the Company ORM object rather than only the company_id.

### Rationale

Avoid repeated database lookups.

Improve readability.

### Consequences

Future services can directly access company properties.

---

# ADR-007

## Title

Session-Based JWT Validation

### Status

Accepted

### Decision

JWT authentication includes persistent session validation.

### Rationale

Allows immediate session revocation.

### Consequences

Revoked sessions immediately lose API access.

---

# ADR-008

## Title

Soft Delete Strategy

### Status

Accepted

### Decision

Business entities use soft deletes.

Historical records remain immutable.

### Rationale

Preserve audit history.

### Consequences

Attendance and Occupancy records are never deleted.

---

# ADR-009

## Title

Immutable Migration Policy

### Status

Accepted

### Decision

Applied Alembic migrations are immutable.

Corrections require new migrations.

### Rationale

Prevent migration divergence across environments.

### Consequences

Historical migration files are never modified after release.

---

# ADR-010

## Title

RBAC Documentation Before Authorization

### Status

Accepted

### Decision

Authorization implementation requires an approved RBAC Matrix.

### Rationale

Prevent undocumented permission models.

### Consequences

PermissionChecker and authorization logic cannot be implemented until RBAC documentation is finalized.

---

# ADR-011

## Title

AI-Assisted Development

### Status

Accepted

### Decision

AI assists implementation.

Architectural decisions remain human-approved.

### Rationale

Prevent undocumented assumptions.

### Consequences

AI must stop and report Documentation Gaps instead of inventing business rules.

---

# ADR-012

## Title

Subcontractor Company Identity Model

### Status

Accepted

### Decision

A Subcontractor Company is a business entity.

It is not an authentication role.

Individual users authenticate using standard user roles.

### Rationale

Organizations do not log in.

People do.

### Consequences

Authentication and authorization remain consistent across all companies.

---

# Future ADRs

All future architectural decisions must be appended.

Existing ADRs should never be rewritten.

If an architectural decision changes:

- Mark the previous ADR as Superseded.
- Create a new ADR explaining the new decision.

Architecture history must remain traceable.

---


