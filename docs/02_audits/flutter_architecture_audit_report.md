# ConstructPulse - Flutter Architecture Audit Report

**Date:** July 2026  
**Auditor:** Senior Flutter Architect  
**Scope:** `mobile/` (Flutter / Riverpod / GoRouter)

This report evaluates the engineering quality of the Flutter application architecture. Findings are based exclusively on verified repository evidence.

---

## 1. Project Architecture & Feature Boundaries

### Observation: Leaking Domain Boundaries
**Evidence:** In `features/attendance/presentation/providers/attendance_providers.dart`, the file explicitly imports `dashboard/presentation/screens/admin_dashboard_screen.dart` and `dashboard/presentation/providers/occupancy_providers.dart`. The `AttendanceNotifier` manually invalidates dashboard and occupancy providers upon check-in/check-out.
**Engineering Risk:** This violates Feature-First and Clean Architecture principles. Features should be isolated. Hard-coupling `attendance` to `dashboard` creates circular dependencies and makes the Attendance feature impossible to extract or test in isolation.
**Recommendation:** Use an event bus, or have the Dashboard providers watch the Attendance state and invalidate themselves Reactively, rather than Attendance imperatively invalidating Dashboard.
**Priority:** 🔴 Critical

---

## 2. State Management

### Observation: Improper Async State Handling in UI
**Evidence:** In `live_attendance_screen.dart`, the `build` method calculates the live duration using `final duration = DateTime.now().difference(record.checkInTime);`. 
**Engineering Risk:** Because `DateTime.now()` is evaluated once during the build phase, the duration string (e.g., "1.5h") will remain completely static on the screen. It will not tick upward unless the user manually triggers a pull-to-refresh to force a rebuild.
**Recommendation:** Create a custom `Ticker` widget or use a `StreamProvider.autoDispose` that emits a new `DateTime` every minute to trigger isolated widget rebuilds for live durations.
**Priority:** 🟠 High

---

## 3. Repository Layer & Networking

### Observation: Absence of Retrofit Code Generation
**Evidence:** Despite previous documentation claiming the migration to "Retrofit 10" was complete, `features/attendance/data/repositories/attendance_repository.dart` and `auth_repository.dart` are entirely hand-written. They use raw `_dio.post(...)` and manual JSON mapping (`Attendance.fromJson(response.data)`). No `*.g.dart` generated files exist for Retrofit API clients.
**Engineering Risk:** Hand-written API clients and DTO mappings are highly susceptible to typos, null-pointer exceptions, and drift from the Swagger specification. 
**Recommendation:** Actually implement Retrofit (`@RestApi`) and JSON Serializable (`@JsonSerializable`) to generate the API clients and model parsing.
**Priority:** 🔴 Critical

### Observation: Inefficient Client-Side Data Filtering
**Evidence:** In `attendance_repository.dart` (`getTodayAttendance`), the app fetches the *entire* attendance history for a user via `ApiEndpoints.userAttendance(userId)`, and then manually filters for "today" in Dart memory using `list.where((a) => a.checkInTime.year == now.year...)`.
**Engineering Risk:** As a worker's tenure grows, fetching hundreds of historical records just to display today's status will consume massive bandwidth and parse time, severely impacting app performance and battery life.
**Recommendation:** Implement query parameters on the backend (e.g., `?date=today`) and have the Flutter repository request only the necessary data.
**Priority:** 🟠 High

---

## 4. Routing

### Observation: Fragile Path-Based Navigation
**Evidence:** `core/router/app_router.dart` uses `GoRoute` definitions without the `name:` property. Across the app (e.g., `sites_list_screen.dart`), navigation is triggered using raw string interpolation: `context.push('/sites/${s.id}')`. 
**Engineering Risk:** Hardcoded strings are brittle. Changing a route path in `app_router.dart` will not throw compile-time errors, leading to silent runtime crashes when users click buttons pointing to outdated string paths.
**Recommendation:** Define an enum for all routes (e.g., `AppRoute.siteDetail.name`) and use `context.goNamed(...)` to ensure type-safe routing.
**Priority:** 🟡 Medium

### Observation: Authentication Interceptor Swallow
**Evidence:** In `core/network/api_client.dart`, the `AuthInterceptor` attempts to refresh a token on 401. If the refresh fails, it clears local storage but does *not* redirect the user to the login screen or explicitly trigger the `authProvider` logout method (except for the specific 'Inactive user' payload). 
**Engineering Risk:** The user will be left on a dead screen where API calls silently fail with 401s, but the UI remains "logged in".
**Recommendation:** Wire the interceptor to a global navigation key or stream that forces the `authProvider` into an `unauthenticated` state globally when refresh fails.
**Priority:** 🔴 Critical

---

## 5. Widget & Theme Architecture

### Observation: Massive Inline Widget Trees
**Evidence:** In `sites_list_screen.dart` and `live_attendance_screen.dart`, the `ListView.builder` returns massive inline `Container` and `Card` blocks spanning 50+ lines of layout code.
**Engineering Risk:** Decreased readability, poor reusability, and larger build contexts. It prevents granular rebuilds (e.g., passing a specific `site` to a `const SiteCard(site)` allows Flutter to cache the widget).
**Recommendation:** Extract complex list items into separate stateless widgets (e.g., `SiteListItem`, `AttendanceCard`).
**Priority:** 🟡 Medium

### Observation: Hardcoded Theme Colors
**Evidence:** Widgets directly reference custom color singletons, e.g., `color: AppColors.surface` and `color: AppColors.textTertiary`, rather than using `Theme.of(context).colorScheme.surface`.
**Engineering Risk:** By bypassing the standard `Theme.of(context)` context lookup, the application completely breaks Flutter's built-in support for dynamic theming, accessibility high-contrast modes, and seamless Dark Mode toggling.
**Recommendation:** Map `AppColors` into a proper `ThemeData.light().colorScheme` and `ThemeData.dark().colorScheme`, and retrieve colors contextually via `Theme.of(context)`.
**Priority:** 🟠 High

---

## 6. Maintainability

### Observation: Lack of Code Generation Ecosystem
**Evidence:** No `.g.dart` or `.freezed.dart` files are visible in the core directories. Providers are hand-written (`FutureProvider.autoDispose`) instead of using `riverpod_generator` (`@riverpod`). 
**Engineering Risk:** The Flutter ecosystem relies heavily on code generation for immutability (Freezed), DI (Riverpod Generator), and Networking (Retrofit). Ignoring these tools drastically increases boilerplate and technical debt.
**Recommendation:** Adopt the modern Flutter generation stack to guarantee immutability, type-safety, and boilerplate reduction.
**Priority:** 🟠 High
