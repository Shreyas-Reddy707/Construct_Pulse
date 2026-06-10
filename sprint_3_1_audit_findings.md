# Sprint 3.1: Root Cause Analysis

## Issue 1: Raw Exception Messages Exposed to Users
* **Observed Behavior:** Workers receive raw strings like `AppException(FORBIDDEN): Worker not assigned to this site`.
* **Root Cause:** The `AppException` class (in `core/errors/exceptions.dart`) explicitly overrides the `toString()` method to output the format `'AppException($code): $message'`. The `mapDioException` correctly intercepts and translates backend errors, but UI components (like `QRScanScreen`) use `$e` or `e.toString()` inside SnackBars to display the error rather than accessing `e.message`.
* **Remediation:** Update `AppException.toString()` to return just the `message`, or modify UI error handlers to conditionally check `if (e is AppException)` and extract `e.message`.

## Issue 2: Worker Sites Screen Shows "No sites found"
* **Observed Behavior:** Worker checks in, dashboard shows the assigned site, but the Sites screen is empty.
* **Root Cause:** The Sites screen utilizes `sitesProvider`, which calls `GET /api/v1/sites/`. Prior to recent stabilization, this backend endpoint (`read_sites` in `backend/app/api/endpoints/sites.py`) for workers incorrectly queried a deprecated `models.Worker` table. Because that table was empty, the query always returned `[]`. Conversely, the Dashboard was able to display the assigned site because it bypassed the `/sites/` endpoint, extracting the site name directly from the check-in attendance summary payload (`summary['site_name']`). 
* **Remediation:** Already addressed during Sprint 3 stabilization by updating the backend `read_sites` function to evaluate `Site.assigned_workers.any(User.id == current_user.id)`.

## Issue 3: Worker Attendance History Empty
* **Observed Behavior:** Check-ins succeed and are visible to admins, but the worker's own Attendance History remains empty.
* **Root Cause:** Caching and provider mapping failure. The `AttendanceHistoryScreen` consumes `workerAttendanceHistoryProvider` (a Riverpod `family` provider) for targeted worker history. When a worker successfully checks in or out, the `AttendanceNotifier` triggers `_invalidateProviders()`. This function successfully invalidates the generic `attendanceHistoryProvider` but completely fails to invalidate the parameterized `workerAttendanceHistoryProvider`. This leaves the worker's history provider with a stale, empty cache.
* **Remediation:** Modify `AttendanceNotifier._invalidateProviders()` in `attendance_providers.dart` to invalidate `workerAttendanceHistoryProvider` using `_ref.invalidate(workerAttendanceHistoryProvider)` (or avoid relying on the family provider for the authenticated worker).

## Issue 4: Dashboard User Status Count Mismatch
* **Observed Behavior:** Admin dashboard shows 22 Total Workers, but the status breakdown shows 21 Approved, 0 Pending, 0 Suspended. One worker is missing.
* **Root Cause:** The `WorkerStatus` enum in `backend/app/models/models.py` defines four states: `PENDING`, `APPROVED`, `REJECTED`, and `SUSPENDED`. In `backend/app/api/endpoints/dashboard.py`, the `get_dashboard_summary` function calculates `total_workers` using `users_query.count()` (which counts all users in the tenant). However, it only performs breakdowns for `PENDING`, `APPROVED`, and `SUSPENDED` statuses. The single missing worker has a `REJECTED` status, which is included in the total but completely omitted from the breakdown calculation.
* **Remediation:** Update the `get_dashboard_summary` endpoint to explicitly calculate and return `rejected_workers = users_query.filter(User.status == WorkerStatus.REJECTED).count()`.
