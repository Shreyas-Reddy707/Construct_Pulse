# ConstructPulse Role-Based Access Control (RBAC) Matrix

**Document ID:** CP-RBAC-001  
**Version:** 1.0  
**Status:** Draft (Architecture Approval Pending)  
**Owner:** ConstructPulse Engineering  
**Last Updated:** July 2026

---

# 1. Purpose

This document defines the authorization architecture for ConstructPulse.

It establishes:

- Roles
- Permission Groups
- Permissions
- Authorization principles
- Visibility rules
- Multi-tenant access rules

This document is the authoritative source of truth for authorization.

No authorization logic may be implemented unless defined here.

---

# 2. Authorization Architecture

ConstructPulse follows a Role-Based Access Control (RBAC) model.

Authorization hierarchy:

User

↓

Role

↓

Permission Group

↓

Permission

Users never receive direct permissions.

Roles receive Permission Groups.

Permission Groups contain individual Permissions.

---

# 3. Design Principles

The authorization model follows:

- Least Privilege
- Explicit Authorization
- Multi-Tenant Isolation
- Separation of Duties
- Business Capability Based Permissions
- No Direct User Permissions

---

# 4. Role Hierarchy

The organizational hierarchy is:

Platform Owner

↓

Company Administrator

↓

Operations Manager

↓

Site Manager

↓

Supervisor

↓

Worker

Visitor

---

## Important

Hierarchy does NOT imply permission inheritance.

Permissions must always be granted explicitly.

---

# 5. Roles

## Platform Owner

Platform-wide administration.

Responsible for:

- Platform configuration
- Company provisioning
- Platform analytics
- Subscription management

Cannot:

- Participate as workforce
- Mark attendance

---

## Company Administrator

Responsible for:

- Company configuration
- Workforce management
- Site creation
- Manager assignment
- Emergency configuration

---

## Operations Manager

Responsible for:

- Operational oversight
- Workforce allocation
- Attendance monitoring
- Site coordination

Cannot:

- Modify company configuration
- Create Company Administrators

---

## Site Manager

Responsible for:

- Site operations
- Daily workforce
- Attendance supervision
- Safety compliance

Cannot:

- Access unrelated sites
- Modify company settings

---

## Supervisor

Responsible for:

- Crew supervision
- Attendance verification
- Incident reporting

Cannot:

- Create users
- Approve administrators
- Modify sites

---

## Worker

Responsible for:

- QR attendance
- Safety induction
- Assigned work
- Personal profile

Cannot perform administrative functions.

---

## Visitor

Temporary access only.

Permissions are assigned according to the approved business process.

---

# 6. Permission Groups

The documentation confirms Permission Groups exist.

The canonical Permission Group definitions remain under architecture review.

Current Status:

Documentation Gap DG-001

Implementation of Permission Groups is prohibited until approved.

---

# 7. Permissions

Permissions follow the standard format:

resource.action

Examples:

attendance.view

attendance.check_in

attendance.check_out

worker.create

worker.update

site.create

reports.view

Permission definitions will be expanded as business modules are finalized.

---

# 8. Role Assignment Rules

Each authenticated user has exactly one primary Role.

Roles may not assign permissions directly.

Permissions are inherited through Permission Groups.

No user may assign a role equal to or higher than their own.

---

# 9. Visibility Rules

Platform Owner

Platform-wide visibility.

Company Administrator

Visibility limited to their Company.

Operations Manager

Visibility limited to assigned operational scope.

Site Manager

Visibility limited to assigned Sites.

Supervisor

Visibility limited to assigned crews.

Worker

Visibility limited to personal information and assigned Sites.

---

# 10. Multi-Tenant Rules

Every authorization decision executes within the authenticated Company context.

Cross-tenant access is prohibited.

Platform Owner is the only exception.

---

# 11. Authorization Principles

Authorization is evaluated for every protected request.

Authentication does not imply authorization.

Permission evaluation must be explicit.

Authorization must never rely on client-side validation.

---

# 12. Implementation Rules

The Authorization Engine must implement:

- PermissionChecker
- Role validation
- Tenant validation
- Permission resolution

No endpoint may bypass authorization.

---

# 13. Documentation Gaps

The following remain unresolved:

DG-001

Permission Group definitions.

DG-002

Role → Permission Group assignments.

DG-003

permission_version derivation.

DG-004

Undocumented administrative roles.

DG-005

Optional administrative attendance.

These gaps must be resolved before Authorization Engine implementation.

---

# 14. Future Evolution

Future modules will extend this document rather than replacing it.

Examples:

- Asset Management
- Equipment
- Payroll
- Inventory
- Procurement
- Compliance
- Analytics

All future permissions must follow:

resource.action

Naming standards.

---


