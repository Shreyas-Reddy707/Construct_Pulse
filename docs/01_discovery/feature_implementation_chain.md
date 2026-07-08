# ConstructPulse - Complete Feature Implementation Chain

This document contains a verified, exhaustive trace of the implementation chain for every feature in the ConstructPulse repository. It maps exact file names, classes, routes, schemas, and models.

---

## 1. Attendance

**UI Screen(s)**
- `qr_scan_screen.dart` (`QrScanScreen`)
- `live_attendance_screen.dart` (`LiveAttendanceScreen`)
- `attendance_history_screen.dart` (`AttendanceHistoryScreen`)

**Provider(s)**
- `attendance_providers.dart` (`attendanceProvider`, `liveAttendanceProvider`)

**Repository**
- `attendance_repository.dart` (`AttendanceRepository`)

**API Client**
- Uses generic Dio client configured in `core/network/api_client.dart`

**Domain Entities (Dart)**
- `attendance.dart` (`Attendance`)
- `attendance_summary.dart` (`AttendanceSummary`)

**Backend Endpoint(s)**
- `/attendance/check-in` (`attendance.py`)
- `/attendance/check-out` (`attendance.py`)

**Input/Output DTOs & Schemas (Python)**
- `AttendanceCheckIn`, `AttendanceCheckOut`, `AttendanceResponse` (in `schemas.py`)

**Service(s)**
- `attendance_service.py` (`AttendanceService`)

**Database Model(s)**
- `Attendance` (in `models.py`)

**Database Table(s)**
- `attendance`

**Related Features**
- Auth, Sites, Occupancy, Reporting, Workforce

---

## 2. Auth

**UI Screen(s)**
- `splash_screen.dart` (`SplashScreen`)
- `login_screen.dart` (`LoginScreen`)
- `otp_verification_screen.dart` (`OtpVerificationScreen`)
- `registration_screen.dart` (`RegistrationScreen`)
- `pending_approval_screen.dart` (`PendingApprovalScreen`)
- `rejected_screen.dart` (`RejectedScreen`)

**Provider(s)**
- `auth_provider.dart` (`authProvider`, `AuthProviderNotifier`)

**Repository**
- `auth_repository.dart` (`AuthRepository`)
- `firebase_auth_service.dart` (`FirebaseAuthService`)

**API Client**
- Uses generic Dio client configured in `core/network/api_client.dart`

**Domain Entities (Dart)**
- `user.dart` (`User`)

**Backend Endpoint(s)**
- `/auth/login` (`auth.py`)

**Input/Output DTOs & Schemas (Python)**
- `FirebaseLogin`, `Token`, `UserResponse`, `UserCreate` (in `schemas.py`)

**Service(s)**
- `identity_mapper.py` (`IdentityMapper`)
- `authorization_service.py` (`AuthorizationService`)

**Database Model(s)**
- `User`, `Role` (in `models.py`)

**Database Table(s)**
- `users`, `roles`

**Related Features**
- Company, Workforce

---

## 3. Company

**UI Screen(s)**
- `companies_list_screen.dart` (`CompaniesListScreen`)
- `company_detail_screen.dart` (`CompanyDetailScreen`)
- `departments_list_screen.dart` (`DepartmentsListScreen`)
- `contractors_list_screen.dart` (`ContractorsListScreen`)
- `create_company_screen.dart` (`CreateCompanyScreen`)

**Provider(s)**
- `company_providers.dart` (`companyListProvider`, `departmentListProvider`, `contractorListProvider`)

**Repository**
- `company_repository.dart` (`CompanyRepository`)

**API Client**
- Uses generic Dio client configured in `core/network/api_client.dart`

**Domain Entities (Dart)**
- `company.dart` (`Company`)
- `department.dart` (`Department`)
- `contractor.dart` (`Contractor`)

**Backend Endpoint(s)**
- `/companies` (`companies.py`)
- `/departments` (`departments.py`)
- `/contractors` (`contractors.py`)

**Input/Output DTOs & Schemas (Python)**
- `CompanyCreate`, `CompanyResponse`, `DepartmentCreate`, `DepartmentResponse`, `ContractorCreate`, `ContractorResponse` (in `schemas.py`)

**Service(s)**
- Standard CRUD logic via FastAPI Depends/Session (No explicit `company_service.py` evident; logic resides in routers or generic base repositories)
- `registration_service.py` (`RegistrationService` for tenant provisioning)

**Database Model(s)**
- `Company`, `Department`, `Contractor` (in `models.py`)

**Database Table(s)**
- `companies`, `departments`, `contractors`

**Related Features**
- Auth, Sites, Workforce

---

## 4. Dashboard

**UI Screen(s)**
- `admin_dashboard_screen.dart` (`AdminDashboardScreen`)
- `manager_dashboard_screen.dart` (`ManagerDashboardScreen`)
- `worker_dashboard_screen.dart` (`WorkerDashboardScreen`)
- `analytics_screen.dart` (`AnalyticsScreen`)

**Provider(s)**
- `occupancy_providers.dart` (`dashboardProvider`) (Note: shares occupancy providers)

**Repository**
- `occupancy_repository.dart` (`OccupancyRepository`)

**API Client**
- Uses generic Dio client configured in `core/network/api_client.dart`

**Domain Entities (Dart)**
- `occupancy_stats.dart` (`OccupancyStats`)

**Backend Endpoint(s)**
- `/dashboard` (`dashboard.py`)

**Input/Output DTOs & Schemas (Python)**
- `OccupancyDashboard`, `SafetyDashboard`, `MusterDashboard` (in `schemas.py`)

**Service(s)**
- Aggregation endpoints (calls `occupancy_service.py`, `attendance_service.py`, `incident_service.py`)

**Database Model(s)**
- Cross-entity aggregations (no single dashboard model).

**Database Table(s)**
- Multiple (`attendance`, `occupancy_snapshots`, `incidents`)

**Related Features**
- Occupancy, Attendance, Safety, Emergency

---

## 5. Emergency (Muster)

**UI Screen(s)**
- `emergency_muster_screen.dart` (`EmergencyMusterScreen`)

**Provider(s)**
- Unknown (Not explicitly defined in presentation/providers, likely using generic state or local widget state for now).

**Repository**
- Unknown (Not explicitly defined in data/repositories, likely using direct Dio calls or pending implementation).

**API Client**
- Uses generic Dio client configured in `core/network/api_client.dart`

**Domain Entities (Dart)**
- Unknown (Not explicitly defined in domain/entities for mobile yet).

**Backend Endpoint(s)**
- `/muster` (`emergency_muster.py`)

**Input/Output DTOs & Schemas (Python)**
- `MusterSessionCreate`, `MusterSessionResponse`, `MusterParticipantResponse`, `MusterSummary`, `MusterOverrideRequest` (in `schemas.py`)

**Service(s)**
- `emergency_muster_service.py` (`EmergencyMusterService`)

**Database Model(s)**
- `MusterSession`, `MusterParticipant`, `MusterAuditLog` (in `models.py`)

**Database Table(s)**
- `muster_sessions`, `muster_participants`, `muster_audit_logs`

**Related Features**
- Sites, Occupancy, Dashboard

---

## 6. Notifications

**UI Screen(s)**
- `notifications_screen.dart` (`NotificationsScreen`)

**Provider(s)**
- Unknown (Pending mobile implementation).

**Repository**
- Unknown (Pending mobile implementation).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Unknown (Pending).

**Backend Endpoint(s)**
- `/notifications` (`notifications.py`)

**Input/Output DTOs & Schemas (Python)**
- (Implicit in `models.py`: `NotificationType`, `NotificationPriority`, `RecipientStatus`, `NotificationSource`)

**Service(s)**
- `notification_service.py` (`NotificationService`)

**Database Model(s)**
- `Notification`, `NotificationRecipient`, `NotificationAuditLog` (in `models.py`)

**Database Table(s)**
- `notifications`, `notification_recipients`, `notification_audit_logs`

**Related Features**
- Safety Communication

---

## 7. Occupancy

**UI Screen(s)**
- `occupancy_dashboard_screen.dart` (`OccupancyDashboardScreen`)

**Provider(s)**
- `occupancy_providers.dart` (`occupancyProvider`)

**Repository**
- `occupancy_repository.dart` (`OccupancyRepository`)

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- `occupancy_summary.dart` (`OccupancySummary`)

**Backend Endpoint(s)**
- `/occupancy` (`occupancy.py`)

**Input/Output DTOs & Schemas (Python)**
- `OccupancyQuery`, `OccupancySummary`, `DepartmentOccupancy`, `ContractorOccupancy`, `OccupancyDashboard`, `OccupancySnapshotResponse` (in `schemas.py`)

**Service(s)**
- `occupancy_service.py` (`OccupancyService`)

**Database Model(s)**
- `OccupancySnapshot` (in `models.py`)

**Database Table(s)**
- `occupancy_snapshots`

**Related Features**
- Attendance, Dashboard, Sites

---

## 8. Payroll

**UI Screen(s)**
- `payroll_preview_screen.dart` (`PayrollPreviewScreen`)

**Provider(s)**
- Unknown (Pending mobile implementation).

**Repository**
- Unknown (Pending mobile implementation).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Unknown (Pending).

**Backend Endpoint(s)**
- `/payroll` (`payroll.py`)

**Input/Output DTOs & Schemas (Python)**
- (Implicit in `models.py`: `PayrollStatus`, `AdjustmentType`, `PayrollSource`)

**Service(s)**
- `payroll_service.py` (`PayrollService`)

**Database Model(s)**
- `PayrollRun`, `PayrollEmployee`, `PayrollAdjustment`, `PayrollAuditLog` (in `models.py`)

**Database Table(s)**
- `payroll_runs`, `payroll_employees`, `payroll_adjustments`, `payroll_audit_logs`

**Related Features**
- Attendance, Workforce

---

## 9. Planning

**UI Screen(s)**
- `daily_plan_screen.dart` (`DailyPlanScreen`)

**Provider(s)**
- Unknown (Pending).

**Repository**
- Unknown (Pending).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Unknown.

**Backend Endpoint(s)**
- `/planning` (`planning.py`)

**Input/Output DTOs & Schemas (Python)**
- (Implicit in `models.py`: `PlanStatus`, `PlanSource`)

**Service(s)**
- `workforce_plan_service.py` (`WorkforcePlanService`)

**Database Model(s)**
- `WorkforcePlan`, `WorkforcePlanDepartment`, `WorkforcePlanContractor`, `WorkforcePlanAuditLog` (in `models.py`)

**Database Table(s)**
- `workforce_plans`, `workforce_plan_departments`, `workforce_plan_contractors`, `workforce_plan_audit_logs`

**Related Features**
- Sites, Company

---

## 10. Profile

**UI Screen(s)**
- `profile_screen.dart` (`ProfileScreen`)

**Provider(s)**
- Unknown (Shares `auth_provider.dart` for user state).

**Repository**
- Unknown (Shares `auth_repository.dart`).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Uses `User` (from `auth/domain/entities`).

**Backend Endpoint(s)**
- `/users/me` (`users.py`)

**Input/Output DTOs & Schemas (Python)**
- `UserResponse` (in `schemas.py`)

**Service(s)**
- Internal routing logic via `deps.get_current_user`.

**Database Model(s)**
- `User` (in `models.py`)

**Database Table(s)**
- `users`

**Related Features**
- Auth

---

## 11. Reports

**UI Screen(s)**
- `reports_screen.dart` (`ReportsScreen`)

**Provider(s)**
- Unknown (Pending).

**Repository**
- Unknown (Pending).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Unknown.

**Backend Endpoint(s)**
- `/reporting` (`reporting.py`)
- `/attendance/report` (`attendance_reporting.py`)

**Input/Output DTOs & Schemas (Python)**
- `AttendanceReportQuery`, `AttendanceReportResponse`, `ReportMetadata`, `AttendanceReportRow` (in `schemas.py`)

**Service(s)**
- `reporting_service.py` (`ReportingService`)
- `attendance_reporting_service.py` (`AttendanceReportingService`)

**Database Model(s)**
- `ComplianceReport`, `ComplianceReportSnapshot`, `ReportAuditLog` (in `models.py`)

**Database Table(s)**
- `compliance_reports`, `compliance_report_snapshots`, `report_audit_logs`

**Related Features**
- Attendance, Safety, Payroll

---

## 12. Sites

**UI Screen(s)**
- `sites_list_screen.dart` (`SitesListScreen`)
- `site_create_screen.dart` (`SiteCreateScreen`)
- `site_detail_screen.dart` (`SiteDetailScreen`)
- `site_occupancy_screen.dart` (`SiteOccupancyScreen`)
- `site_qr_screen.dart` (`SiteQrScreen`)

**Provider(s)**
- `site_providers.dart` (`siteListProvider`, `currentSiteProvider`)

**Repository**
- `site_repository.dart` (`SiteRepository`)

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- `site.dart` (`Site`)

**Backend Endpoint(s)**
- `/sites` (`sites.py`)

**Input/Output DTOs & Schemas (Python)**
- `SiteCreate`, `SiteUpdate`, `SiteResponse`, `SiteAssignment`, `QRCodeResponse` (in `schemas.py`)

**Service(s)**
- `site_readiness_service.py` (`SiteReadinessService`)
- `secure_token_service.py` (`SecureTokenService` for QR logic)

**Database Model(s)**
- `Site`, `SiteQRCode` (in `models.py`)

**Database Table(s)**
- `sites`, `site_qr_codes`

**Related Features**
- Company, Attendance, Occupancy

---

## 13. Tasks

**UI Screen(s)**
- `task_list_screen.dart` (`TaskListScreen`)

**Provider(s)**
- Unknown (Pending mobile implementation).

**Repository**
- Unknown (Pending mobile implementation).

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Unknown.

**Backend Endpoint(s)**
- Unknown (No clear `tasks.py` endpoint mapped in `api.py`. Likely handled by `safety_operations.py` via Corrective Actions or pending future integration).

**Input/Output DTOs & Schemas (Python)**
- Unknown.

**Service(s)**
- Unknown.

**Database Model(s)**
- Unknown.

**Database Table(s)**
- Unknown.

**Related Features**
- Safety Operations (Corrective Actions)

---

## 14. Workforce

**UI Screen(s)**
- `workforce_directory_screen.dart` (`WorkforceDirectoryScreen`)
- `worker_detail_screen.dart` (`WorkerDetailScreen`)

**Provider(s)**
- `worker_providers.dart` (`workerListProvider`)
- `worker_action_provider.dart` (`WorkerActionNotifier`)

**Repository**
- `worker_repository.dart` (`WorkerRepository`)

**API Client**
- Uses generic Dio client.

**Domain Entities (Dart)**
- Maps to `User` (from Auth domain) or generic UI states.

**Backend Endpoint(s)**
- `/users` (`users.py`)
- `/register` (`registration.py`)
- `/registrations` (`registrations.py` for approval queues)
- `/qualifications` (`qualifications.py`)

**Input/Output DTOs & Schemas (Python)**
- `WorkerReadinessResponse`, `WorkerQualificationCreate`, `WorkerQualificationResponse`, `RegistrationRequestResponse` (in `schemas.py`)

**Service(s)**
- `worker_readiness_service.py` (`WorkerReadinessService`)
- `qualification_service.py` (`QualificationService`)
- `approval_service.py` (`ApprovalService`)

**Database Model(s)**
- `User`, `WorkerInductionRecord`, `WorkerQualification`, `RegistrationRequest` (in `models.py`)

**Database Table(s)**
- `users`, `worker_inductions`, `worker_qualifications`, `registration_requests`

**Related Features**
- Auth, Company, Sites

---

## 15. Additional Backend-Only Features (Safety & Visitors)

*These features have robust backend implementations but lack dedicated root folders in `mobile/lib/features/`.*

### Safety (Incidents & Observations)
**Backend Endpoint(s)**: `/incidents` (`incidents.py`), `/safety` (`safety.py`, `safety_operations.py`), `/communications` (`safety_communication.py`)
**Input/Output DTOs & Schemas**: `IncidentCreate`, `IncidentResponse`, `SafetyObservationCreate`, `SafetyObservationResponse`, `CommunicationCreate`
**Service(s)**: `incident_service.py`, `safety_operations_service.py`, `safety_communication_service.py`
**Database Model(s)**: `Incident`, `SafetyObservation`, `SafetyCommunication`
**Database Table(s)**: `incidents`, `safety_observations`, `safety_communications`

### Visitors
**Backend Endpoint(s)**: `/visitors` (`visitors.py`)
**Input/Output DTOs & Schemas**: `VisitorVisitCreate`, `VisitorVisitResponse`, `VisitorDashboard`
**Service(s)**: `visitor_service.py`
**Database Model(s)**: `VisitorVisit`, `VisitorAuditLog`
**Database Table(s)**: `visitor_visits`, `visitor_audit_logs`
