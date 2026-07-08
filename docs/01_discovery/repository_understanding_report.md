# ConstructPulse - Repository Understanding Report

## 1. High-Level Architecture
ConstructPulse is an enterprise-grade mobile application and backend service built for construction workforce management. It relies on a decoupled client-server model:
- **Backend**: A RESTful Python application built with FastAPI.
- **Frontend**: A cross-platform mobile application built with Flutter.
- **Database**: PostgreSQL database.
- **Identity Provider**: Firebase Authentication (Phone/OTP).

The platform embraces multi-tenancy, providing data isolation between distinct construction companies, while also supporting hierarchical groupings like Departments and Contractors.

## 2. Backend Architecture
The backend is a monolithic FastAPI application employing a classic **Layered/Clean Architecture** approach:
- **`app/api/endpoints`**: Thin controllers (routers) responsible for HTTP request/response handling and payload validation via Pydantic.
- **`app/services`**: The core business logic layer. The codebase favors "Thick Services, Thin Controllers" (e.g., `AttendanceService`, `OccupancyService`, `RegistrationService`).
- **`app/models`**: SQLAlchemy ORM models representing the database schema.
- **`app/schemas`**: Pydantic schemas enforcing input validation and output serialization.
- **`app/core`**: Security utilities (JWT validation, Firebase token parsing), configuration, and centralized logging.
- **`app/db`**: Database session management and connection pooling.

## 3. Flutter Architecture
The Flutter mobile application uses a **Feature-First Domain-Driven Design (DDD)** structure:
- **`lib/core`**: Contains shared application infrastructure, including routing, networking (`api_client.dart`), secure storage, theming, and common widgets.
- **`lib/features`**: Vertical slices of functionality (e.g., `attendance`, `auth`, `company`, `dashboard`, `sites`, `workforce`).
- **Inside each feature**:
  - `data/repositories/`: Interfaces with the backend APIs.
  - `domain/entities/`: Dart representations of business objects.
  - `presentation/providers/`: State management for the feature.
  - `presentation/screens/`: UI views.

## 4. Authentication Flow
1. **Frontend**: The user submits their phone number. Firebase Auth handles OTP generation and SMS delivery.
2. **Verification**: The user enters the OTP. Upon success, Firebase issues a Firebase ID Token.
3. **Backend Handshake**: The mobile app sends the Firebase ID Token to the FastAPI backend (`/auth/login`).
4. **Session Creation**: The backend validates the Firebase token (via Firebase Admin SDK), finds or creates the corresponding user record, and issues a proprietary backend JWT (Bearer Token).
5. **Authorization**: Subsequent API requests use the backend JWT, which enforces Role-Based Access Control (RBAC) and company-level tenant isolation.

## 5. API Layer
The FastAPI endpoints are organized by domain:
- **`/auth`**: Login, OTP verification, and JWT issuance.
- **`/users` & `/workforce`**: Worker directory and lifecycle management.
- **`/sites`**: Construction site configuration and QR code generation.
- **`/attendance`**: Secure check-in/out via QR tokens.
- **`/occupancy`**: Live dashboard metrics and aggregations.
- **`/emergency_muster`**: Triggering and reporting on emergency evacuations.
- **`/safety` & `/incidents`**: Incident logging and safety communications.

## 6. Repository Layer
- **Backend**: Data access is primarily embedded within the `app/services` layer using SQLAlchemy ORM sessions directly (e.g., querying `db.query(Attendance)`). There is no strict separate "Repository" abstraction on the backend; the service layer acts as the repository.
- **Frontend**: Explicit Repository classes (`AuthRepository`, `AttendanceRepository`) abstract the networking logic away from the UI. They utilize Dio/Retrofit to make HTTP calls to the backend and serialize the JSON responses into Dart Domain Entities.

## 7. Database Structure
A robust relational schema deployed on PostgreSQL:
- **Identity & Tenancy**: `Company`, `Department`, `Contractor`, `User`, `Role`, `Permission`.
- **Operations**: `Site`, `SiteQRCode`, `Attendance`, `AttendanceCorrectionLog`.
- **Safety**: `Incident`, `IncidentEvidence`, `MusterSession`, `MusterParticipant`.
- **Compliance**: `WorkerInductionRecord`, `WorkerQualification`.
- **Design Patterns**: 
  - Widespread use of `UUID` strings for primary keys.
  - Widespread adoption of a `SoftDeleteMixin` (`is_deleted`, `deleted_at`) for safe data archival.
  - Comprehensive Audit Logs for sensitive domains (e.g., `AttendanceCorrectionLog`, `MusterAuditLog`, `IncidentAuditLog`).

## 8. State Management
The Flutter application strictly uses **Riverpod** (via `flutter_riverpod`).
- Providers are located in `lib/features/*/presentation/providers/`.
- Modern Riverpod constructs (e.g., `Notifier`, `@riverpod` annotations, `ref.onDispose`) are heavily utilized, ensuring reactive UI updates and clean separation of UI from business logic.

## 9. Navigation
Navigation is managed declaratively using **GoRouter**.
- **`app_router.dart`**: Defines all application routes.
- **Shell Routes**: Implementation of shell architectures (`app_shell.dart`, `worker_shell.dart`, `company_admin_shell.dart`) to support persistent bottom navigation bars customized by user role.
- **Guards**: `auth_guard.dart` ensures unauthenticated users are redirected to the splash or login screens.

## 10. Feature Modules
The mobile app is partitioned into clear, cohesive modules:
- `auth`: Login, OTP, Registration logic.
- `company`: Tenant administration, department/contractor lists.
- `sites`: Geofences, site management, QR generation.
- `workforce`: Worker directory, approvals, profiles.
- `attendance`: QR scanning, history, live check-ins.
- `occupancy`: Dashboard stats and demographic breakdowns.
- `emergency`: Mustering and safety accountability.
- `dashboard`, `notifications`, `payroll`, `planning`, `profile`, `reports`, `tasks`.

## 11. Shared Components
Located in `lib/core/`:
- **Theme**: `app_colors.dart`, `app_theme.dart`, `app_typography.dart` enforcing a unified brand design system.
- **Widgets**: `buttons.dart`, `kpi_card.dart`, `common_widgets.dart` to prevent UI code duplication.
- **Network**: Standardized Dio interceptors and API response wrappers.

## 12. Current Implementation Status
- **Overall Completion**: ~78%
- **Phase**: Phase 2 (Enterprise Workforce Platform Foundation) is in progress.
- **Sprints**: Sprints 1-4 are certified and complete. The project is currently staged to begin **Sprint 5**.

## 13. Completed Features
- Multi-tenant architecture and tenant isolation.
- Authentication (OTP) and RBAC governance.
- Site lifecycle management (Draft -> Active).
- Secure Presence Verification (QR tokens, GPS validation).
- Registration and Identity approval queues.
- Attendance lifecycle (Check-in/out, Administrative Checkout, Corrections).
- Live Occupancy tracking and snapshot generation.

## 14. Partially Completed Features
- **Operations & Safety**: The backend ORM models for `Incident`, `MusterSession`, and `SafetyObservation` exist in the database schema, but these modules are officially slated for the upcoming Sprint 5. The Flutter app has UI shells (`emergency_muster_screen.dart`), indicating they are works in progress.

## 15. Missing Features (Future Roadmap)
- Advanced Analytics Dashboard.
- Automated Payroll Integration (stubs exist).
- Geofenced Check-ins (currently uses GPS validation, but full passive geofencing is planned).
- Mobile Offline Mode with Synchronization.
- Operations Intelligence (Planning Engine, Resource Allocation).

## 16. Development Philosophy
Inferred from analyzing the architecture and documentation:
1. **Security & Governance First**: Heavy reliance on audit trails, optimistic concurrency (`version` integers on models), secure temporary tokens, and immutable governance logs.
2. **Clean separation of concerns**: Distinct feature folders in Flutter, explicit service layers in FastAPI. 
3. **Data Integrity**: Soft deletes prevent accidental data loss.
4. **Scalability**: Multi-tenant RBAC design ensures the platform can scale to hundreds of contractors securely.

## Areas with Incomplete Understanding
- **Hardware Integration**: It is unclear if there are physical turnstiles/kiosks integrated, or if attendance is purely handled via mobile app QR scanning.
- **Reporting Engine**: The backend has an `attendance_reporting_service.py` with CSV export, but it's unclear what rendering engine (if any) is used for complex PDF reports.
