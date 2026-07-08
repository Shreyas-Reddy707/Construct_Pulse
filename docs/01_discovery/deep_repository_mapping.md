# ConstructPulse - Deep Repository Mapping

This document serves as the definitive engineering reference manual for the ConstructPulse repository. It maps the technical structure, dependencies, state management, and implementation status as of July 2026.

---

## 1. Repository Inventory

| Location | Responsibility |
|----------|----------------|
| `backend/app/` | Core FastAPI application. Contains endpoints, services, schemas, and models. |
| `backend/alembic/` | Database migrations and revision scripts. |
| `mobile/lib/` | Primary Flutter application source code. |
| `mobile/lib/core/` | Shared frontend infrastructure (routing, network, theme, secure storage). |
| `mobile/lib/features/` | Feature-first Domain-Driven Design modules (Auth, Attendance, Sites, etc.). |
| `docs/` | Architectural Decisions (ADRs), API Specifications, DB Design, and Technical Debt registers. |
| `docs/governance/` | RBAC matrices and official technical debt documentation. |
| `mobile/android/` & `mobile/ios/` | Native application shells and build configurations. |

---

## 2. Backend Dependency Map

| Feature Area | Router (`api/endpoints/`) | Service (`services/`) | Models | Tables |
|--------------|---------------------------|-----------------------|--------|--------|
| **Auth** | `auth.py` | `identity_mapper.py`, `authorization_service.py` | `User`, `Role` | `users`, `roles` |
| **Companies**| `companies.py`, `departments.py`, `contractors.py` | `registration_service.py` | `Company`, `Department`, `Contractor` | `companies`, `departments`, `contractors` |
| **Sites** | `sites.py` | `site_readiness_service.py` | `Site`, `SiteQRCode` | `sites`, `site_qr_codes` |
| **Attendance**| `attendance.py`, `attendance_governance.py`, `attendance_reporting.py` | `attendance_service.py`, `attendance_governance_service.py` | `Attendance`, `AttendanceCorrectionLog` | `attendance`, `attendance_correction_logs` |
| **Occupancy**| `occupancy.py` | `occupancy_service.py` | `OccupancySnapshot` | `occupancy_snapshots` |
| **Emergency**| `emergency_muster.py` | `emergency_muster_service.py` | `MusterSession`, `MusterParticipant` | `muster_sessions`, `muster_participants` |
| **Safety** | `safety.py`, `incidents.py`, `safety_operations.py` | `safety_service.py`, `incident_service.py` | `Incident`, `SafetyObservation` | `incidents`, `safety_observations` |
| **Reporting**| `reporting.py` | `reporting_service.py` | `ComplianceReport` | `compliance_reports` |
| **Payroll** | `payroll.py` | `payroll_service.py` | `PayrollRun`, `PayrollEmployee` | `payroll_runs`, `payroll_employees` |

---

## 3. Frontend Dependency Map

| Feature | Screens | Providers | Repositories | Domain Entities |
|---------|---------|-----------|--------------|-----------------|
| **Auth** | `LoginScreen`, `OtpVerificationScreen`, `RegistrationScreen` | `auth_provider` | `AuthRepository` | `User` |
| **Company** | `CompaniesListScreen`, `DepartmentsListScreen` | `company_provider` | `CompanyRepository` | `Company`, `Department` |
| **Sites** | `SitesListScreen`, `SiteDetailScreen`, `SiteQrScreen` | `site_provider` | `SiteRepository` | `Site` |
| **Attendance** | `QrScanScreen`, `LiveAttendanceScreen`, `AttendanceHistoryScreen` | `attendance_provider` | `AttendanceRepository` | `AttendanceSummary` |
| **Occupancy** | `SiteOccupancyScreen` | `occupancy_provider` | `OccupancyRepository` | `OccupancyDashboard` |
| **Emergency** | `EmergencyMusterScreen` | `muster_provider` | `MusterRepository` | `MusterSession` |
| **Workforce** | `WorkforceDirectoryScreen`, `WorkerDetailScreen` | `workforce_provider` | `WorkforceRepository` | `Worker` |
| **Dashboard** | `ManagerDashboardScreen`, `AnalyticsScreen` | `dashboard_provider` | `DashboardRepository` | `KPI` |

---

## 4. API Inventory (Core Endpoints)

| Method | Route | Purpose | Roles | Input | Output |
|--------|-------|---------|-------|-------|--------|
| POST | `/auth/login` | Authenticate user via Firebase Token | Any | `FirebaseLogin` | `Token` |
| POST | `/attendance/check-in` | Record worker entry | Worker | `AttendanceCheckIn` | `AttendanceResponse` |
| POST | `/attendance/check-out` | Record worker exit | Worker | `AttendanceCheckOut`| `AttendanceResponse` |
| POST | `/sites/` | Create a new construction site | Admin | `SiteCreate` | `SiteResponse` |
| GET | `/occupancy/` | Fetch live occupancy data | Admin/Manager | Query Params | `OccupancyDashboard` |
| POST | `/muster/` | Initiate emergency evacuation | Admin/Safety | `MusterSessionCreate`| `MusterSessionResponse`|
| POST | `/incidents/` | Report a new safety incident | Any | `IncidentCreate` | `IncidentResponse` |
| GET | `/reporting/` | Generate compliance report | Admin | Query Params | `AttendanceReportResponse`|

---

## 5. Database Relationship Map

*All tables utilize UUID primary keys and `SoftDeleteMixin` (`is_deleted`, `deleted_at`) unless specified otherwise.*

| Table | Purpose | Relationships | Audit Logging |
|-------|---------|---------------|---------------|
| `companies` | Multi-tenant root entity | Parent of `users`, `departments`, `sites` | No |
| `users` | Identity management | Belongs to `company`, `department` | No |
| `sites` | Geofenced work locations | Belongs to `company` | No |
| `attendance` | Secure presence records | References `user`, `site` | Yes (`attendance_correction_logs`) |
| `incidents` | Safety incidents | References `site`, `user` (reporter) | Yes (`incident_audit_logs`) |
| `muster_sessions` | Emergency evacuations | References `site` | Yes (`muster_audit_logs`) |
| `payroll_runs` | Financial integrations | References `company`, `site` | Yes (`payroll_audit_logs`) |
| `compliance_reports` | Immutable data snapshots | References `company` | Yes (`report_audit_logs`) |

---

## 6. State Ownership Map (Frontend)

| State Scope | Ownership | Description |
|-------------|-----------|-------------|
| **Global State** | `ProviderScope` | Root container for Riverpod. |
| **Session State** | `authProvider`, `FlutterSecureStorage` | Manages JWT, User Identity, and RBAC roles. Overrides route guards. |
| **Feature State** | `[feature]Provider` | Feature-specific business logic (e.g., `attendanceProvider` for check-in state). |
| **Widget-local** | `StatefulWidget` / `hooks` | Ephemeral UI state (e.g., text field inputs, tab selection, scroll positions). |

---

## 7. Feature Dependency Matrix

| Feature | Depends On | Used By | Backend Dependencies |
|---------|------------|---------|----------------------|
| **Auth** | Core Network | All Features | `auth.py`, `Firebase` |
| **Sites** | Core | Attendance, Occupancy, Muster | `sites.py` |
| **Attendance** | Auth, Sites | Occupancy, Payroll, Reporting | `attendance.py` |
| **Occupancy** | Attendance, Sites| Dashboard | `occupancy.py` |
| **Emergency** | Sites, Workforce | Dashboard | `emergency_muster.py` |
| **Dashboard** | All Features | App Shell (UI) | `dashboard.py` |

---

## 8. Folder Responsibility Matrix

| Folder | Purpose | Allowed Dependencies |
|--------|---------|----------------------|
| `backend/app/api` | Request validation & routing | `app.schemas`, `app.services` |
| `backend/app/services` | Business logic & DB access | `app.models`, `app.db` |
| `backend/app/models` | SQLAlchemy ORM definitions | Standard library |
| `mobile/lib/core` | Global infrastructure | External packages (Dio, Riverpod) |
| `mobile/lib/features/*`| Domain-specific logic | `lib/core`, external packages. Avoid cross-feature dependencies if possible. |

---

## 9. Technical Debt Register

*Sourced from repository evidence and `docs/governance/TECHNICAL_DEBT.md`*

- **Open (TD-001):** `permission_version` Placeholder in JWT.
- **Open (TD-002):** Temporary `firebase_uid` placeholder for Company Administrators.
- **Planned (TD-003):** Authorization Engine implementation pending.
- **Open (TD-004):** RBAC Matrix approval pending.
- **Planned (TD-005):** Firebase Authentication Integration incomplete.
- **Open (TD-006):** Pending Safety Foundation Migration (blocked by ENUM issues).
- **Codebase Todos:** "TODO: Move the rest of this into files in ephemeral" (`mobile/linux/flutter/CMakeLists.txt`), "TODO: Specify your own unique Application ID" (`mobile/android/app/build.gradle.kts`).
- **Deprecated Code:** `CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS` in iOS project; Legacy direct user creation endpoint in `backend/app/api/endpoints/auth.py` marked `@router.post("/register", deprecated=True)`.

---

## 10. Implementation Heatmap

Based on repository evidence (presence of schemas, models, services, and UI screens).

| Feature | Backend Status | Frontend Status | Overall Completeness Estimate |
|---------|----------------|-----------------|-------------------------------|
| **Core Architecture** | Complete | Complete | **100%** |
| **Auth & Identity** | Complete | Complete | **95%** (Firebase Auth pending) |
| **Site Management** | Complete | Complete | **95%** |
| **Attendance & Governance** | Complete | Complete | **95%** |
| **Occupancy & Dashboard** | Complete | Complete | **90%** |
| **Emergency Muster** | Complete | Partial (UI Shells) | **60%** |
| **Safety & Incidents** | Complete | Partial | **50%** |
| **Compliance Reporting** | Complete | Missing | **40%** |
| **Payroll Foundation** | Models/Services exist | Missing | **30%** |
| **Platform Configuration** | Models/Services exist | Missing | **20%** |
