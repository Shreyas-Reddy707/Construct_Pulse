# ConstructPulse Domain Map

**Version:** 1.1  
**Status:** Active Development  
**Owner:** ConstructPulse Core Team  
**Last Updated:** YYYY-MM-DD

---

# 1. Purpose

ConstructPulse follows a **Domain-Oriented Architecture**.

Each domain represents a distinct business capability and owns its own:

- Business Rules
- Database Models
- Service Layer
- API Endpoints
- Operational Workflows
- Future Evolution

Domains should remain as independent as practical while collaborating through clearly defined service interfaces.

---

# 2. Domain Hierarchy

```text
ConstructPulse

├── Platform Domain
├── Organization Domain
├── Worker Domain
├── Site Domain
├── Access Control Domain
├── Attendance Domain
├── Occupancy Domain
├── Emergency Domain
├── Reporting & Analytics Domain
└── Administration Domain
```

---

# 3. Platform Domain

## Purpose

Provides the foundational infrastructure used by every other domain.

## Responsibilities

- Authentication
- Authorization
- RBAC
- Multi-Tenant Isolation
- JWT Security
- Platform Configuration
- Security Policies

## Primary Services

- AuthorizationService

## Primary Models

- User
- Role
- Permission
- PermissionGroup
- Session

## Status

🟡 Foundation Complete

---

# 4. Organization Domain

## Purpose

Manage construction organizations and their operational hierarchy.

## Responsibilities

- Companies
- Departments
- Contractors
- Organizational Structure
- Company Configuration

## Primary Models

- Company
- Department
- Contractor

## Status

🟡 Foundation Complete

---

# 5. Worker Domain

## Purpose

Manage the complete operational lifecycle of workers.

## Responsibilities

- Registration
- Identity
- Approval
- Operational Readiness
- Safety
- Professional Qualifications
- Compliance Passport

## Primary Services

- WorkerReadinessService
- SafetyService
- QualificationService

## Primary Models

- User
- QualificationType
- QualificationRequirement
- WorkerQualification
- InductionPackage
- WorkerInductionRecord

## Current Status

✅ Complete

---

# 6. Site Domain

## Purpose

Manage construction sites throughout their operational lifecycle.

## Responsibilities

- Site Creation
- Site Configuration
- Lifecycle Management
- Activation
- Suspension
- Archival
- Operational Readiness

## Primary Services

- SiteReadinessService

## Primary Models

- Site

## Current Status

✅ Complete

---

# 7. Access Control Domain

## Purpose

Control and verify physical access to construction sites.

Attendance is a consequence of successful access verification.

The Access Control Domain is responsible for determining whether an individual is permitted to enter a site and perform operational activities.

---

## Responsibilities

- Dynamic QR Token Management
- QR Validation
- GPS Validation
- Identity Resolution
- Universal Registration
- Worker Verification
- Visitor Registration
- Approval Queue
- Assignment Validation
- Presence Verification
- Entry Authorization

---

## Planned Services

- AccessVerificationService
- QRService
- RegistrationService
- ApprovalQueueService

---

## Planned Models

- SiteQRCode
- RegistrationRequest
- ApprovalRequest

---

## Current Status

⏳ In Progress

---

# 8. Attendance Domain

## Purpose

Record workforce attendance after successful access verification.

## Responsibilities

- Check-In
- Check-Out
- GPS Confirmation
- Attendance History
- Attendance Validation

## Planned Services

- AttendanceService

## Current Status

⏳ Planned

---

# 9. Occupancy Domain

## Purpose

Provide live visibility into workforce presence.

## Responsibilities

- Live Occupancy
- Workforce Count
- Occupancy History
- Site Presence

## Planned Services

- OccupancyService

## Current Status

⏳ Planned

---

# 10. Emergency Domain

## Purpose

Provide emergency accountability and response.

## Responsibilities

- Emergency Muster
- Worker Accountability
- Emergency Contacts
- Incident Coordination

## Planned Services

- EmergencyService

## Current Status

⏳ Planned

---

# 11. Reporting & Analytics Domain

## Purpose

Provide operational intelligence.

## Responsibilities

- Dashboards
- Attendance Reports
- Workforce Reports
- Compliance Reports
- Safety Analytics
- Productivity Analytics

## Planned Services

- ReportingService

## Current Status

⏳ Planned

---

# 12. Administration Domain

## Purpose

Provide enterprise administration capabilities.

## Responsibilities

- Subscription Management
- Billing
- Platform Configuration
- Audit Management
- Feature Flags
- System Administration

## Planned Services

- AdministrationService

## Current Status

⏳ Planned

---

# 13. Domain Dependency Map

```text
Platform
    │
    ▼
Organization
    │
    ▼
Worker
    │
    ▼
Site
    │
    ▼
Access Control
    │
    ▼
Attendance
    │
    ▼
Occupancy
    │
    ▼
Emergency
    │
    ▼
Reporting & Analytics

Administration
│
└── Cross-Cutting Across Every Domain
```

---

# 14. Operational Decision Gates

ConstructPulse centralizes major operational decisions through dedicated business services.

## Current Decision Gates

### WorkerReadinessService

Determines whether a worker is operationally ready.

---

### SiteReadinessService

Determines whether a construction site is operationally ready.

---

## Future Decision Gates

### AccessVerificationService

Determines whether an individual is authorized to enter a construction site.

---

### AttendanceService

Determines whether attendance may be successfully recorded.

---

### EmergencyService

Determines workforce accountability during emergency events.

---

# 15. Delivery Mapping

| Domain | Phase | Sprint | Batch |
|----------|--------|---------|--------|
| Platform Foundation | Phase 1 | Sprint 1–2 | Foundation |
| Organization Foundation | Phase 1 | Sprint 2 | Organization |
| Worker Domain | Phase 2 | Sprint 3 | Batch 1A–1D |
| Site Domain | Phase 2 | Sprint 3 | Batch 2 |
| Access Control Domain | Phase 2 | Sprint 3 | Batch 3A–3D |
| Attendance Domain | Phase 2 | Sprint 4 | Batch 4A–4B |
| Occupancy Domain | Phase 2 | Sprint 4 | Batch 5 |
| Emergency Domain | Phase 2 | Sprint 5 | Batch 6 |
| Reporting & Analytics | Phase 3 | TBD | TBD |
| Administration | Phase 4 | TBD | TBD |

---

# 16. Architecture Principles

Every domain must:

- Own its own business rules.
- Keep controllers thin.
- Centralize business logic in services.
- Follow multi-tenant isolation.
- Enforce RBAC.
- Minimize coupling.
- Remain independently testable.

Cross-domain interactions should occur through service interfaces rather than duplicating business logic.

---

# 17. Future Evolution

The architecture intentionally supports future expansion without redesign.

Potential future domains and capabilities include:

- Equipment Management
- Asset Tracking
- Procurement
- Vendor Management
- Payroll Integration
- Inventory Management

Future Access Control enhancements:

- NFC Access
- BLE Beacons
- Face Recognition
- Biometric Verification
- Device Trust
- Polygon Geofencing
- Offline Presence Verification

Future Intelligence:

- AI Workforce Insights
- Predictive Analytics
- Resource Optimization
- Safety Risk Prediction
- Productivity Forecasting

