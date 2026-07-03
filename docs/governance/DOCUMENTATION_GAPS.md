# ConstructPulse Documentation Gaps

**Document ID:** CP-DG-001  
**Version:** 1.0  
**Status:** Active  
**Owner:** ConstructPulse Engineering  
**Last Updated:** July 2026

---

# Purpose

This document records gaps, ambiguities, and undocumented architectural or business requirements discovered during the development of ConstructPulse.

A Documentation Gap is **not a bug**.

It is a missing or incomplete business or technical specification that prevents a fully documented implementation.

Developers and AI-assisted implementation **must not invent solutions** for documented gaps.

Instead:

1. Record the gap.
2. Pause implementation if the gap affects architecture or business behaviour.
3. Resolve the gap through an Architecture Decision Record (ADR) or updated documentation.
4. Resume implementation.

---

# Documentation Gap Workflow

Whenever documentation is incomplete:

Documentation

↓

Gap Identified

↓

Record Documentation Gap

↓

Architecture Review

↓

Decision

↓

Documentation Updated

↓

Implementation

---

# Gap Status Definitions

| Status | Meaning |
|---------|----------|
| Open | Awaiting architectural decision |
| In Review | Under discussion |
| Resolved | Architecture approved and documented |
| Closed | Fully implemented |

---

# DG-001

## Title

RBAC Permission Group Definitions

### Status

Open

### Description

The documentation specifies that:

Role

↓

Permission Group

↓

Permission

However, it does not define:

- Permission Group names
- Permission Group responsibilities
- Permission Group boundaries

### Impact

Authorization Foundation

Authorization Engine

Permission seeding

### Resolution Required

Approve the canonical Permission Groups in RBAC_MATRIX.md.

---

# DG-002

## Title

Role → Permission Group Assignments

### Status

Open

### Description

The documentation defines platform roles but does not define which Permission Groups belong to each role.

### Impact

Authorization

PermissionChecker

Route protection

### Resolution Required

Approve the role matrix in RBAC_MATRIX.md.

---

# DG-003

## Title

Permission Version Source

### Status

Open

### Description

JWT contains a permission_version claim.

The documentation does not specify how this value is generated.

Possible sources include:

- Role
- Permission Group
- Permission Matrix
- Global Version

No official source is documented.

### Impact

JWT

Authorization

Permission cache

### Resolution Required

Architecture Decision required.

---

# DG-004

## Title

Undocumented Administrative Roles

### Status

Open

### Description

The following roles appear in documentation but do not have fully documented responsibilities or permissions:

- Visitor
- Company Director
- Project Manager
- Safety Officer

### Impact

RBAC

Authorization

Future modules

### Resolution Required

Business ownership required.

---

# DG-005

## Title

Optional Administrative Attendance

### Status

Open

### Description

Documentation marks Check-In and Check-Out as optional for administrative roles.

Configuration rules are undocumented.

### Impact

Attendance

Authorization

Mobile Application

### Resolution Required

Business rule definition required.

---

# Future Documentation Gaps

All future undocumented behaviour, architecture, workflows, or business rules must be recorded here.

Implementation must never fill documentation gaps through assumptions.

---

# Engineering Rule

Documentation Silence ≠ Permission to Design.

When in doubt:

Stop.

Document.

Review.

Approve.

Then implement.

---


