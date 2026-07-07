# Flutter ↔ Backend Integration Readiness Audit

## 1. Executive Summary
**Overall Status:** **PASS WITH IMPLEMENTATION WORK**

The Flutter application's internal architecture is highly capable of consuming the existing FastAPI backend. However, the integration itself is currently in a fragmented state. While core features (Attendance, Occupancy, Company) have fully wired integration layers (Repositories and DTO mappings), the majority of the MVP scope (Safety, Incidents, Visitors, etc.) lacks frontend repository coverage completely. Furthermore, there are genuine API incompatibilities in the Registration and Site DTOs that will cause immediate HTTP 422 errors and null-rendering bugs if executed in their current state.

---

## 2. Authentication Integration
- **Login Flow:** The backend correctly processes the Firebase token, and Flutter successfully persists the resulting `access_token` into `SecureStorageService`.
- **Authorization Headers:** Injected successfully on all non-public routes via `AuthInterceptor`.
- **Session Restoration:** **PARTIAL.** Flutter's `AuthInterceptor` is fully equipped to catch 401s and call `/api/v1/auth/refresh`, but the backend login endpoint does not return a `refresh_token`, causing Flutter to log the user out instead.
- **Logout Flow:** Because the backend is stateless (JWT), Flutter correctly clears local storage without making an API call.

---

## 3. API & Repository Coverage
The Flutter repository layer currently only maps to a fraction of the available backend APIs:

**Implemented Repositories:**
- `AuthRepository`
- `AttendanceRepository`
- `CompanyRepository`
- `OccupancyRepository`
- `SiteRepository`
- `WorkerRepository`

**Missing Repositories (Not Started):**
- Muster, Visitors, Incidents, Safety, Safety Communication, Notifications, Planning, Payroll, Reporting, Configuration.

---

## 4. DTO Compatibility
An inspection of the JSON mapping between the Backend schemas and Flutter entities reveals several inconsistencies:

- **Registration DTO (Blocker):** Flutter's `AuthRepository.register` sends `first_name`, `last_name`, and `phone`. The Backend's `UserCreate` schema inherits from `UserBase`, which strictly requires `name` and `phone_number`. This guarantees an HTTP 422 Validation Error upon registration.
- **Site DTO (Bug):** The Backend `SiteResponse` returns the site's physical location under the key `location`. Flutter's `Site.fromJson` explicitly looks for the key `address`. Consequently, all sites will render with `null` addresses on mobile.
- **User DTO (Compatible):** The Backend returns `name` and `phone_number`. Flutter intelligently patches this via `json['first_name'] ?? json['name']?.split(' ').first` and `json['phone_number'] ?? json['phone']`, gracefully absorbing the API inconsistency.
- **Attendance DTO (Compatible):** The Backend returns additional fields (`gps_latitude`, `check_in_method`), which Flutter safely ignores due to its manual deserialization approach.

---

## 5. Retrofit Coverage
- **Status:** **NOT USED**
- Although `retrofit` is declared in the `pubspec.yaml`, the Flutter application strictly utilizes raw `Dio` instances for API calls (e.g., `_dio.get(ApiEndpoints.sites)`). Therefore, there are no generated `@RestApi` interfaces to audit. The API integration is entirely manual.

---

## 6. Feature Integration Matrix

| Feature | Backend | Flutter Integration | Status |
| :--- | :--- | :--- | :--- |
| **Authentication** | READY | READY | **PARTIAL** *(Registration mismatch)* |
| **Sites** | READY | READY | **PARTIAL** *(Location mapping bug)* |
| **Attendance** | READY | READY | **READY** |
| **Workers/Company** | READY | READY | **READY** |
| **Occupancy** | READY | READY | **READY** |
| **Emergency Muster** | READY | MISSING | **NOT STARTED** |
| **Visitors** | READY | MISSING | **NOT STARTED** |
| **Incidents** | READY | MISSING | **NOT STARTED** |
| **Safety Operations** | READY | MISSING | **NOT STARTED** |
| **Payroll/Planning** | READY | MISSING | **NOT STARTED** |

---

## 7. Verified Integration Risks
1. **Registration 422 Error:** The `first_name` vs `name` and `phone` vs `phone_number` payload mismatch between Flutter and FastAPI will completely block user onboarding.
2. **Missing Frontend Repositories:** The Flutter team has massive scope remaining just to wire up the API clients for 10 missing MVP modules. Because they use manual `Dio` requests and manual `fromJson` mapping, this will require significant boilerplate effort compared to using Retrofit.

---

## 8. Sprint 7 Readiness
The architecture is theoretically ready, but the actual integration state requires immediate implementation work. Before creating UI screens for the missing modules, the engineering team must align the Registration and Site DTOs and establish the missing Data/Domain repositories.

---

## 9. Certification

**PASS WITH IMPLEMENTATION WORK**

**Justification:** The integration mechanisms (Dio, Interceptors, Riverpod) are robust. However, the application cannot "Pass" flawlessly because genuine data contract mismatches exist that will crash core flows (Registration). Furthermore, over 50% of the backend features remain entirely unintegrated on the client side. The team must correct the DTO mismatches as the first task of Sprint 7.

---

**Audit Integrity Confirmation**
- Source files modified: 0
- Source files created: 0
- Source files deleted: 0
- Documentation files created: 1 (`FLUTTER_BACKEND_INTEGRATION_READINESS_AUDIT.md`)
- Repository code changed: No
