# ConstructPulse Engineering Decision Register (EDR)

This document is the master engineering register consolidating findings from the Repository Mapping, Documentation Verification, Backend Architecture, Backend Production Engineering, Flutter Architecture, and Flutter UI Engineering audits.

---

## Backend Architecture

### EDR-001: Inconsistent Router Thinness
- **Category:** Backend Architecture
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** `api/endpoints/users.py` contains 150+ lines of inline cross-domain business logic, breaking the "Thin Controllers" pattern.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Partially Correct
- **Business Impact:** Negatively impacts maintainability, architectural consistency, reusability, and future testing. Does not currently affect correctness, security, or data integrity.
- **Complexity:** Medium
- **Engineering Decision:** Improve Before MVP (No implementation performed at this stage)
- **Verification Notes:** The architectural concern is valid. The placement of cross-domain business logic, attendance mutations, and transaction persistence inside the routing layer breaks the "Thick Services, Thin Controllers" architecture.

### EDR-002: Brittle Database Connection String Parsing
- **Category:** Backend Architecture
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** Database engine initialization relies on `.replace("postgresql://", "postgresql+psycopg://")` which will fail silently if the DSN format changes.
- **Priority:** 🟢 Low
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Very Low. Creates a deployment portability concern for alternative DSN formats, but has no impact on application correctness, security, or runtime performance.
- **Complexity:** Low
- **Engineering Decision:** Post-MVP. The concern only affects future deployment flexibility across different infrastructure providers. No implementation is performed at this stage.
- **Verification Notes:** The audit finding is technically correct. The string replacement creates operational fragility during deployments to new environments. However, there is no impact on the current MVP.

---

## Backend Production Engineering

### EDR-003: Delegated Transaction Ownership Breaking Atomicity
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `get_db` delegates `commit()` to individual services, meaning API endpoints composing multiple services suffer from partial commit failures.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** High. Complex workflows spanning multiple services will result in partial failures and corrupted data states.
- **Complexity:** High
- **Engineering Decision:** Improve Before MVP. The current transaction lifecycle is owned by individual service methods rather than by the request or unit-of-work boundary. No implementation is performed at this stage.
- **Verification Notes:** The audit finding is correct. The risk is structural rather than necessarily observable in today's implementation. It becomes significant as multi-service orchestration grows.

### EDR-004: Broken Atomicity in Atomic Sequences
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `registration_seq` is consumed before database insertion, meaning a failed insert permanently loses the sequence number.
- **Priority:** 🟡 Medium
- **Current Status:** ❌ Reject
- **Verification Result:** Partially Correct
- **Business Impact:** None. Gapless registration numbering is not a documented business or compliance requirement.
- **Complexity:** Not Applicable
- **Engineering Decision:** Reject. The current PostgreSQL sequence implementation should remain unchanged.
- **Verification Notes:** The audit identified expected PostgreSQL behaviour rather than a repository defect. Sequence gaps are required for high concurrency and scalability.

### EDR-005: Check-Then-Act Race Conditions in Registration
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** `detect_duplicates` runs multiple `SELECT` queries before `INSERT`, risking parallel registration duplicates under high load.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** High. Duplicate registrations can enter the approval queue and cause downstream 500 errors.
- **Complexity:** Medium
- **Engineering Decision:** Improve Before MVP. Duplicate prevention relies entirely on application-level SELECT queries without database enforcement. No implementation is performed at this stage.
- **Verification Notes:** The audit correctly identified a TOCTOU race condition. Any database enforcement (e.g., partial unique index) must respect business rules that allow re-registration if prior requests were rejected.

### EDR-006: Incomplete Optimistic Concurrency Control
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Models like `Attendance` and `SafetyObservation` contain a version column but lack SQLAlchemy `__mapper_args__ = {"version_id_col": ...}` mapping.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium. The application is vulnerable to lost-update concurrency conflicts where simultaneous edits may silently overwrite one another.
- **Complexity:** Medium
- **Engineering Decision:** Improve Before MVP. The models define explicit version columns intended for optimistic concurrency control, but the SQLAlchemy ORM is not configured to use them. No implementation is performed at this stage.
- **Verification Notes:** The application is specifically vulnerable to lost-update conflicts. Existing database constraints and transactions continue to function correctly; the missing protection relates only to optimistic concurrency control.

### EDR-007: Suboptimal Idempotency in Approvals
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Approving an already approved request throws a 400 instead of 200/Idempotent, breaking retry logic on poor mobile networks.
- **Priority:** 🟡 Medium
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium. Under unreliable network conditions, an automatic retry generates a false-negative HTTP 400 error despite the underlying operation succeeding.
- **Complexity:** Low
- **Engineering Decision:** Improve Before MVP. The API is not idempotent from a client perspective. Improving idempotency for repeated approval requests will make the mobile application significantly more reliable. No implementation is performed at this stage.
- **Verification Notes:** Idempotent behaviour should apply only to repeated requests representing the same intended business operation. Conflicting state transitions must continue to return appropriate validation errors.

### EDR-008: Synchronous I/O Blocking for Notifications
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** FCM and email notifications block the main API thread during HTTP requests.
- **Priority:** 🔴 Critical
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None.
- **Complexity:** Not Applicable
- **Engineering Decision:** Reject. The current NotificationService only implements in-application notification persistence (writing to the database) without external network communication. The implementation should remain unchanged.
- **Verification Notes:** This decision applies only to the current repository implementation. If future releases introduce external push notifications, email delivery, SMS, or webhook integrations, background processing should be evaluated as part of those new capabilities.

### EDR-009: Ignored Migration Failures at Startup
- **Category:** Backend Production Engineering
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** The application starts successfully even if Alembic migrations fail, causing backend routers to crash on schema mismatches.
- **Priority:** 🟠 High
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Partially Correct
- **Business Impact:** Medium.
- **Complexity:** Medium
- **Engineering Decision:** Post-MVP. The audit correctly identifies that the current health endpoint does not validate database readiness or schema compatibility. However, the reported OperationalError occurs during optional demo data seeding. For the current MVP, this issue does not justify blocking implementation work.
- **Verification Notes:** For enterprise production deployments, dedicated readiness checks should validate critical dependencies before accepting traffic.

---

## Flutter Architecture

### EDR-010: Leaking Domain Boundaries in State Management
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** `attendance_providers.dart` tightly couples domains by explicitly importing and mutating dashboard/occupancy state, violating Clean Architecture.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Medium
- **Engineering Decision:** Improve Before MVP. The Attendance feature directly imports and invalidates providers belonging to other feature domains. This introduces unnecessary architectural coupling and violates the intended Feature-First architecture. No implementation is performed at this stage.
- **Verification Notes:** The current implementation functions correctly. This recommendation focuses on long-term architectural maintainability rather than correcting a runtime defect. Any future implementation should be performed as a coordinated state-management refactor.

### EDR-011: Improper Async State Handling for Live Data
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture & UI Engineering Audits
- **Audit Summary:** Live attendance durations evaluate `DateTime.now()` directly in the build method without a stream/ticker, causing stagnant UI strings.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Low
- **Engineering Decision:** Improve Before MVP. The Live Attendance screen calculates elapsed work duration using DateTime.now() during widget build without any mechanism to trigger periodic rebuilds. The issue is isolated to the presentation layer; backend timestamps remain accurate. No implementation is performed at this stage.
- **Verification Notes:** The issue affects only UI freshness. Future implementation should update only the duration widgets periodically instead of rebuilding the entire screen to preserve Flutter rendering efficiency.

### EDR-012: Complete Absence of Code Generation (False Retrofit Migration)
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit & Documentation Verification
- **Audit Summary:** Despite claims of a Retrofit 10 & Freezed migration, core repositories use raw, error-prone `Dio` and manual `.fromJson()` methods with zero `.g.dart` generated files.
- **Priority:** 🔴 Critical
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** High.
- **Engineering Decision:** Post-MVP. The current implementation is functionally correct. Introducing a repository-wide Retrofit/Freezed migration before MVP completion would create unnecessary engineering churn and increase merge conflict risk. The migration will be performed as a dedicated modernization initiative after MVP completion.
- **Verification Notes:** The current manual networking implementation functions correctly. This recommendation is focused on long-term maintainability rather than correcting a production defect. The migration should be planned as a dedicated modernization sprint after backend contracts and Flutter features stabilize.

### EDR-013: Fragile Path-Based GoRouter Navigation
- **Category:** Flutter Architecture
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** Routing relies entirely on hardcoded string paths rather than typed Route names or enums, increasing runtime crash risks.
- **Priority:** 🟡 Medium
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Medium.
- **Engineering Decision:** Post-MVP. The application relies on raw string-based GoRouter paths. While functionally correct, it lacks compile-time safety. Introducing typed routing before the MVP is complete would create unnecessary engineering churn. The preferred strategy is to stabilize the navigation architecture first and perform a typed-routing migration after MVP completion.
- **Verification Notes:** The current routing implementation is functionally correct. This recommendation focuses on improving long-term maintainability and compile-time safety rather than correcting a production defect.

---

## UI Engineering

### EDR-014: Hardcoded Colors Breaking Material 3 Theming
- **Category:** UI Engineering
- **Source Audit:** Flutter Architecture & UI Engineering Audits
- **Audit Summary:** Widgets manually check brightness and explicitly reference `AppColors.surface` instead of natively hooking into `Theme.of(context).colorScheme`.
- **Priority:** 🔴 Critical
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** High.
- **Engineering Decision:** Post-MVP. The current implementation relies on manually selecting colors and explicit brightness checks instead of leveraging Material 3 ThemeData. It is functionally correct. Migrating the entire UI to ThemeData before MVP completion would introduce unnecessary engineering churn. The preferred strategy is to execute a dedicated UI modernization initiative after MVP completion.
- **Verification Notes:** The current theming implementation functions correctly. This recommendation focuses on improving maintainability and scalability rather than correcting a production defect.

### EDR-015: Typography Configuration Breaking Dark Mode
- **Category:** UI Engineering
- **Source Audit:** Flutter Architecture & UI Engineering Audits
- **Audit Summary:** `AppTypography` statically defines `Colors.black` for default text colors. In dark mode, this forces black text onto dark backgrounds, making text completely unreadable unless manually overridden by `isDark` checks in the widget.
- **Priority:** 🔴 Critical
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** High.
- **Engineering Decision:** Post-MVP. The typography system embeds hardcoded colors directly into AppTypography rather than inheriting through Flutter's TextTheme. It functions correctly because widgets manually override colors. Migrating the typography system now would introduce unnecessary engineering churn. The preferred strategy is to complete feature development and modernize typography together with the broader Material 3 theming initiative after MVP completion.
- **Verification Notes:** The current typography implementation functions correctly. This recommendation focuses on maintainability and future scalability rather than correcting a production defect.

### EDR-016: Rigid 2D Layouts Lacking Responsiveness
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Admin dashboards and list views use hardcoded dimensions, `ListView`, and rigid `Row`/`Column` setups without `LayoutBuilder`, `Wrap`, or responsive breakpoints, breaking heavily on tablets or web.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** High.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. The current dashboard implementation relies on fixed Row and Expanded layouts without adaptive breakpoints or responsive grid logic. ConstructPulse is an enterprise platform expected to be viewed by supervisors on tablets and larger displays. This lack of responsiveness directly impacts perceived quality and user experience.
- **Verification Notes:** The application is currently optimized primarily for portrait mobile layouts. The recommendation focuses on improving the responsiveness of user-facing enterprise dashboards before MVP delivery without requiring a complete UI redesign.

### EDR-017: Missing Interaction Feedbacks
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** `GestureDetector` is used extensively for tappable cards/buttons instead of `InkWell` or `Material`, removing ripple effects and visual touch feedback, making the app feel unresponsive.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Low.
- **Engineering Decision:** Improve Before MVP. The application currently relies on GestureDetector for many interactive widgets, providing no built-in Material interaction feedback. This affects perceived responsiveness and complements EDR-007 by reducing repeated user taps. Because the implementation is localized, low risk, and directly improves UX, it should be completed before the MVP.
- **Verification Notes:** The recommendation is driven primarily by user experience rather than framework compliance. Immediate interaction feedback improves perceived responsiveness, reduces repeated user input under slow network conditions, and complements the idempotency improvements planned in EDR-007.

### EDR-018: "Fake" Static Loading Skeletons
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** `Shimmer` overlays are applied to static hardcoded lists of containers, but these do not dynamically scale to match the actual shape of the data they are loading, causing UI snapping when data loads.
- **Priority:** 🟡 Medium
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None.
- **Complexity:** Not Applicable.
- **Engineering Decision:** Reject. The repository does define a ShimmerBox widget, but a repository-wide review confirms that it is not used anywhere in the active application. Instead, all loading states use standard Material CircularProgressIndicator and LinearProgressIndicator widgets. The audit incorrectly evaluated an implementation that does not exist in the running application.
- **Verification Notes:** The repository contains an unused ShimmerBox component, but it is not part of the active loading experience. Any future decision to introduce shimmer-based skeleton loading should be treated as a separate UX enhancement rather than a correction to this audit finding.

### EDR-019: Missing Semantic Accessibility Wrappers
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Zero `Semantics` widgets wrap visual widgets. Images lack semantic labels, and custom `GestureDetector` buttons fail to announce themselves as buttons to screen readers, violating enterprise accessibility requirements (WCAG/Section 508).
- **Priority:** 🔴 High
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Medium.
- **Engineering Decision:** Post-MVP. The repository currently contains no Semantics widgets or semanticLabel properties, and custom interactive widgets rely primarily on GestureDetector without accessibility annotations. This limits usability for screen reader users and would fail formal accessibility compliance audits. However, ConstructPulse is currently being delivered as an enterprise MVP for client demonstration rather than a certified accessible product. This work should be scheduled after the MVP.
- **Verification Notes:** Accessibility compliance is an important enterprise capability but is not currently a delivery requirement for the ConstructPulse MVP. The absence of semantic annotations does not affect the primary workflows demonstrated to the client. A comprehensive accessibility initiative should be planned after feature completion.

### EDR-020: Massive Inline Widget Sprawl
- **Category:** UI Engineering
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Complex screens (e.g., `AdminDashboardScreen`) write massive nested inline widget trees instead of extracting semantic sub-components, making UI modification highly dangerous.
- **Priority:** 🟡 Medium
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Medium.
- **Engineering Decision:** Post-MVP. Several Flutter presentation screens contain very large build methods with deeply nested widget trees, inline dialogs, Consumers, and layout logic. While this increases maintainability challenges, the implementation is functionally correct and does not block the core enterprise MVP workflows.
- **Verification Notes:** The current implementation prioritizes rapid feature delivery over UI component modularity. Although extracting reusable widgets would improve readability, testing, and future optimization, the existing implementation does not negatively impact correctness. A repository-wide UI componentization initiative should be executed together with the broader Flutter modernization effort after MVP completion.

---

## Security

### EDR-021: Opaque Exception Handling & Domain Bleeding
- **Category:** Security
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** Downstream `ValueError` exceptions are caught uniformly by the router and converted to 400 Bad Requests, destroying stack traces and leaking validation states.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Medium-High.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. The backend currently uses Python's generic ValueError to represent many different categories of business failures. Nearly every FastAPI router catches ValueError and converts it directly into an HTTP 400 response. This causes architectural problems: generic exceptions are used for distinct business conditions, HTTP response codes do not accurately represent failure types, and exception handling logic is duplicated.
- **Verification Notes:** Converting generic ValueError exceptions directly into HTTP 400 responses makes it difficult to distinguish expected business validation failures from unexpected programming errors during production debugging. A future centralized domain exception strategy will improve API consistency, maintainability, and observability without changing business behavior.

### EDR-022: Deprecated Authorization Components Still Active
- **Category:** Security
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** `RoleChecker` is marked deprecated but remains actively utilized by critical endpoints instead of the intended `PermissionChecker`.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** High.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. The repository currently contains two active authorization mechanisms: RoleChecker (deprecated) and PermissionChecker (modern). Although RoleChecker is explicitly marked as deprecated, it is still used across numerous critical API endpoints. This creates inconsistent authorization behavior because some endpoints enforce static role membership while others enforce dynamic permission resolution.
- **Verification Notes:** The current implementation reflects an incomplete migration from role-based authorization to permission-based authorization rather than an abandoned implementation. However, continuing to operate both authorization mechanisms simultaneously creates inconsistent authorization enforcement across the API surface. Completing the migration before the MVP ensures predictable authorization behavior and prevents future endpoints from extending the deprecated pattern.

### EDR-023: Pending Authorization Runtime (RBAC Incomplete)
- **Category:** Security
- **Source Audit:** Backend Architecture Audit & Documentation Verification
- **Audit Summary:** The primary permissions engine is blocked by an unfinalized RBAC matrix, leaving the system functionally insecure for production.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Critical.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. The AuthorizationService and PermissionChecker implementations function correctly. However, the RBAC permission matrix seeded into the database is incomplete. Only the System Admin role is mapped to permission groups, while the remaining operational roles have no permission-group assignments. As a result, PermissionChecker cannot yet replace RoleChecker because most users would resolve to an empty permission set.
- **Verification Notes:** The issue is not an implementation defect in AuthorizationService. The underlying authorization engine operates correctly. The blocker is incomplete authorization configuration data. Completing the RBAC permission matrix is the prerequisite for fully migrating away from the deprecated RoleChecker and enabling enterprise-grade fine-grained authorization.

### EDR-024: Authentication Interceptor Swallow
- **Category:** Security
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** A failed JWT refresh clears secure storage but does not redirect the GoRouter, stranding users on a dead screen with silent 401s.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** High.
- **Complexity:** Low.
- **Engineering Decision:** Improve Before MVP. The AuthInterceptor correctly clears secure storage when JWT refresh fails. However, it does not notify the application's global authentication state by invoking authProvider.logout(). This leaves the client in an inconsistent state where secure storage no longer contains valid credentials while Riverpod continues to believe the user is authenticated.
- **Verification Notes:** The issue is primarily a client-side session lifecycle problem rather than a backend security vulnerability. The backend correctly rejects unauthorized requests. The problem is that the application's authentication state is not synchronized after refresh failure, resulting in a "zombie session" where authenticated screens remain visible despite the loss of valid credentials.

---

## Performance

### EDR-025: Severe N+1 Database Query Risks
- **Category:** Performance
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** The API serializes lazy-loaded relationships (e.g., `user.assigned_sites`) and loops authorization definitions without utilizing `joinedload`.
- **Priority:** 🔴 Critical
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Critical.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. Multiple backend list endpoints return SQLAlchemy ORM entities without eager-loading related models. Pydantic serializes these entities using from_attributes=True while computed model properties access lazy-loaded relationships such as company, department, contractor, and assigned sites. This creates classic N+1 query behavior on large result sets.
- **Verification Notes:** The exact number of generated SQL queries depends on relationship reuse within the SQLAlchemy session and the returned dataset. However, the current architecture is demonstrably vulnerable to N+1 query patterns that can generate hundreds of unnecessary database queries for large list endpoints. Future developers may unintentionally worsen this behavior by adding additional relationship-backed computed properties.

### EDR-026: Expensive In-Memory Backend Aggregations
- **Category:** Performance
- **Source Audit:** Backend Architecture & Production Audits
- **Audit Summary:** The backend computes site-level statistics (attendance, safety, assets) using Python lists and len() rather than SQL COUNT/GROUP BY.
- **Priority:** 🟠 High
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None.
- **Complexity:** Not Applicable.
- **Engineering Decision:** Reject. The verification confirmed that the original audit finding is factually incorrect. The examined backend services consistently perform aggregation inside PostgreSQL using SQLAlchemy database aggregation functions such as func.count(), group_by(), count(), and scalar(). The backend does not load large datasets into Python memory and compute statistics using len(), manual iteration, or list comprehensions as claimed by the audit.
- **Verification Notes:** The repository evidence demonstrates that dashboard and reporting services correctly delegate aggregation work to the database engine. The original audit incorrectly described an architectural anti-pattern that is not present in the current implementation.

### EDR-027: Inefficient Client-Side Data Filtering
- **Category:** Performance
- **Source Audit:** Flutter Architecture Audit
- **Audit Summary:** Flutter `Riverpod` providers download full datasets (e.g., all workers) and filter them entirely in Dart rather than utilizing backend query parameters.
- **Priority:** 🟠 High
- **Current Status:** 🔄 Improve Before MVP
- **Verification Result:** Correct
- **Business Impact:** Critical.
- **Complexity:** Medium.
- **Engineering Decision:** Improve Before MVP. Multiple Flutter screens request complete backend datasets without server-side filtering or pagination. Filtering is then performed entirely inside the client using Dart collection operations such as where() and take(). This causes unnecessary network traffic, excessive JSON parsing, additional memory consumption, and unnecessary client-side computation.
- **Verification Notes:** The issue is most significant for attendance history because historical records grow continuously over time. Rather than requesting filtered datasets from the backend, the application currently downloads the full dataset and discards the majority of it locally. While Out-of-Memory conditions are not guaranteed, increasing dataset sizes will progressively degrade responsiveness, bandwidth usage, and mobile performance.

---

## Documentation

### EDR-028: Missing Offline & Passive Geofencing Capabilities
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** TRD demands offline resilience and background geofencing, but the current app relies strictly on online API requests and manual QR scanning.
- **Priority:** 🟠 High
- **Current Status:** 🟦 New

### EDR-029: Firebase Authentication Flow Discrepancy
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** Architecture docs claim Firebase OTP is active, but implementation relies on placeholders (verified in technical debt).
- **Priority:** 🟡 Medium
- **Current Status:** 🟦 New

### EDR-030: Missing Asset & Fleet Modules
- **Category:** Documentation
- **Source Audit:** Documentation Verification
- **Audit Summary:** API specs define extensive endpoints for assets/machinery that do not exist in the codebase.
- **Priority:** 🟢 Low
- **Current Status:** 📅 Post-MVP
- **Verification Result:** Correct
- **Business Impact:** Medium.
- **Complexity:** Very High.
- **Engineering Decision:** Post-MVP. The verification confirmed that the audit finding is technically correct. The repository documentation defines a comprehensive Asset, Equipment, and Fleet Management domain including workflows, REST APIs, lifecycle documentation, and technical requirements. However, the current codebase contains no implementation of this module. The discrepancy reflects future planned functionality rather than a defect in the existing implementation.
- **Verification Notes:** The documented Asset Management module represents planned product scope rather than incomplete engineering. The existing Workforce, Attendance, Safety, Registration, and Occupancy modules operate independently and are unaffected by the absence of Asset Management. Implementing this domain would constitute a major new feature rather than an engineering correction and should therefore remain outside the MVP implementation scope.

---

## Future Improvements

### EDR-031: Solid Multi-Tenant Isolation
- **Category:** Future Improvements
- **Source Audit:** Backend Architecture Audit
- **Audit Summary:** Excellent dependency injection via `get_current_tenant` guarantees data isolation across companies. Maintain this pattern.
- **Priority:** 🟢 Low
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None (with respect to the audit finding itself).
- **Complexity:** Not Applicable.
- **Engineering Decision:** Reject. The verification confirmed that the original audit conclusion is factually incorrect. The audit claimed that tenant isolation is centrally enforced through the get_current_tenant dependency injection mechanism. Repository analysis demonstrates that this is not the primary architecture. Most endpoint modules enforce tenant isolation manually using explicit company_id filtering or local helper functions. Therefore, the audit's positive assessment of centralized dependency-based tenant isolation is incorrect.
- **Verification Notes:** Although the audit finding is rejected, the verification revealed a separate architectural observation: Tenant isolation is currently enforced manually across many endpoints rather than through a centralized mechanism. This represents a potential future architectural improvement but is outside the scope of this Engineering Decision because the original audit specifically praised an architecture that does not actually exist.

### EDR-032: Robust Security & Rate-Limiting Configuration
- **Category:** Future Improvements
- **Source Audit:** Backend Production Engineering Audit
- **Audit Summary:** Modern implementations of CORS arrays and `slowapi` rate-limiting are properly wired to the environment configuration.
- **Priority:** 🟢 Low
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None (with respect to the audit finding itself).
- **Complexity:** Not Applicable.
- **Engineering Decision:** Reject. The verification confirmed that the original audit conclusion is factually incorrect. The audit claimed that API rate limiting and environment-driven CORS configuration were correctly implemented. Repository analysis shows that slowapi is instantiated but no rate limits are configured, no endpoints use @limiter.limit decorators, and no default rate limits exist. Therefore, no API rate limiting is active. Additionally, BACKEND_CORS_ORIGINS is statically defined in configuration rather than fully environment-driven.
- **Verification Notes:** Although the audit finding is rejected, the verification revealed two independent architectural improvement opportunities: implement functional API rate limiting, and make CORS origins fully environment configurable. These should be tracked independently rather than through this rejected Engineering Decision.

### EDR-033: Standardized Fallback UI Components
- **Category:** Future Improvements
- **Source Audit:** Flutter UI Engineering Audit
- **Audit Summary:** Well-designed `EmptyState` and `ErrorState` components ensure the enterprise app avoids blank white screens during network instability.
- **Priority:** 🟢 Low
- **Current Status:** ❌ Reject
- **Verification Result:** Incorrect
- **Business Impact:** None (with respect to the audit finding itself).
- **Complexity:** Not Applicable.
- **Engineering Decision:** Reject. The verification confirmed that the original audit conclusion is factually incorrect. The audit claimed that reusable EmptyState and ErrorState components are consistently used across the application to provide standardized enterprise-grade loading, empty, and error experiences. Repository analysis demonstrates that although these reusable components exist, they are only utilized in one screen. Most feature modules instead render ad-hoc Text widgets or, in several critical locations, silently return SizedBox() or SizedBox.shrink(), producing blank screens during failures.
- **Verification Notes:** The verification identified a separate architectural improvement opportunity. The application would benefit from standardizing EmptyState and ErrorState usage across all feature modules to provide a consistent user experience. This represents a future UI architecture improvement rather than validation of the original audit conclusion.

---

## EDR Summary Statistics

- **Total Findings:** 33
- **Critical Findings:** 10
- **High Findings:** 11
- **Medium Findings:** 6
- **Low Findings:** 6
