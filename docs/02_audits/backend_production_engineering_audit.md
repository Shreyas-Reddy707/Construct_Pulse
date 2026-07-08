# ConstructPulse - Backend Production Engineering Audit

**Date:** July 2026  
**Auditor:** Senior Backend Architect  
**Scope:** Backend Reliability, Scalability, and Correctness

This document evaluates the production readiness of the FastAPI backend based strictly on verifiable code patterns within the repository.

---

## 1. Database Session Lifecycle

**Observation:** Delegated Transaction Ownership
**Evidence:** `app/db/database.py` defines `get_db()` which yields a session and closes it in a `finally` block, but does *not* call `session.commit()`. Services (e.g., `RegistrationService`, `ApprovalService`) explicitly manage `session.add()` and `session.commit()` themselves.
**Production Risk:** If a single API endpoint invokes multiple service methods sequentially (e.g., `ServiceA.process()` then `ServiceB.process()`), partial failures will occur. `ServiceA`'s commit will be permanently saved to the database even if `ServiceB` throws an exception, breaking data integrity across the request.
**Recommendation:** Enforce transaction boundaries at the Request/Router level via Unit of Work, or configure `get_db()` to manage the commit/rollback lifecycle centrally.
**Priority:** 🔴 Critical

---

## 2. Transaction Boundaries

**Observation:** Broken Atomicity in Atomic Sequences
**Evidence:** In `RegistrationService._generate_registration_number`, the system explicitly executes `session.execute(Sequence('registration_seq'))` before generating the full entity and committing the transaction in `create_request`.
**Production Risk:** If `create_request` fails during database insertion (e.g. unique constraint violation), the sequence number is consumed and permanently lost, resulting in gapless-sequence compliance violations (critical for auditing enterprise registrations).
**Recommendation:** Ensure atomic sequence extraction occurs at the very moment of row insertion, or handle sequence rollbacks gracefully.
**Priority:** 🟡 Medium

---

## 3. Concurrency & Race Conditions

**Observation:** Check-Then-Act Race Conditions in Registration
**Evidence:** `RegistrationService.detect_duplicates()` queries the database for existing phone numbers, and if clear, `create_request()` performs an insert. However, `RegistrationRequest` inside `models.py` has no `UniqueConstraint` on `phone_number`.
**Production Risk:** If a worker double-taps the registration submit button on a slow 3G connection, two identical POST requests can execute simultaneously. Both will pass `detect_duplicates` (since neither has committed yet) and insert two identical registrations into the database.
**Recommendation:** Add a `UniqueConstraint('phone_number', 'status')` or rely on database-level UPSERT capabilities to prevent race conditions.
**Priority:** 🔴 Critical

**Observation:** Incomplete Optimistic Concurrency Control
**Evidence:** The `Attendance` model in `models.py` contains `attendance_version = Column(Integer, default=1)`. However, it lacks SQLAlchemy's mapping argument `__mapper_args__ = {"version_id_col": attendance_version}`.
**Production Risk:** Concurrent admin overrides or checkout updates to the same attendance record will blindly overwrite each other without throwing a `StaleDataError`.
**Recommendation:** Fully wire the version column to SQLAlchemy's optimistic locking mechanism.
**Priority:** 🟠 High

---

## 4. Idempotency

**Observation:** Row-Locked Approval Idempotency
**Evidence:** `ApprovalService.approve_request` explicitly uses `.with_for_update()` to lock the registration row before processing. It then checks `if req.status not in [PENDING, UNDER_REVIEW]: raise 400`.
**Production Risk:** Safe. Concurrent approval requests by two different managers will be serialized at the database level. The first commits; the second acquires the lock, reads the new status, and fails gracefully with a 400.
**Recommendation:** While structurally safe, true REST idempotency should return a 200 OK with the generated User on duplicate retry, rather than throwing a 400 Error.
**Priority:** 🟢 Low

---

## 5. Query Performance

**Observation:** Severe N+1 and Subquery Bottlenecks
**Evidence:** 
- `ApprovalService.fetch_pending_requests` uses an unoptimized `.subquery()` for checking `requested_site_id.in_`.
- As previously noted, relationship lookups (e.g. `user.assigned_sites`) trigger synchronous lazy loads during serialization.
**Production Risk:** At scale, these queries will generate exponential database roundtrips, exhausting connection pools.
**Recommendation:** Implement `joinedload` directives and refactor `.subquery().in_()` to explicit `JOIN` statements.
**Priority:** 🔴 Critical

---

## 6. Scalability

**Observation:** Synchronous Aggregations at Scale
**Evidence:** `AttendanceService.get_my_today_attendance` pulls all rows for a user into memory to loop through and sum `duration`. 
**Production Risk:** While fine for 1 worker, building enterprise-wide dashboards (e.g. for 500 companies with 100,000 active attendance records) using this in-memory python looping architecture will result in Out-Of-Memory (OOM) crashes on the pods.
**Recommendation:** Delegate all heavy aggregations directly to PostgreSQL using `func.sum()` and `group_by`.
**Priority:** 🟠 High

---

## 7. Background Processing

**Observation:** Synchronous I/O Blocking for Notifications
**Evidence:** `NotificationService.create_notification` synchronously loops over all resolved `target_user_ids` and executes `db.add(recipient)` in the main FastAPI request thread. There is no Celery or `BackgroundTasks` implementation.
**Production Risk:** If an emergency broadcast targets 10,000 workers on a site, iterating 10,000 inserts inside a single synchronous HTTP request will trigger gateway timeouts (504s), potentially failing to alert workers in an emergency.
**Recommendation:** Implement a background task queue (Celery/Redis or FastAPI `BackgroundTasks`) for all notification broadcasts. Utilize SQLAlchemy bulk inserts (`insert().values()`) rather than looping `db.add()`.
**Priority:** 🔴 Critical

---

## 8. Observability

**Observation:** Opaque Exception Handling
**Evidence:** Throughout `api/endpoints/`, domain logic throws raw `ValueError` which is caught in a blanket `except ValueError as e: raise HTTPException(400)`.
**Production Risk:** If a downstream service throws a `ValueError` for an unexpected reason (e.g., data casting), it is immediately transformed into a 400 Bad Request without logging a stack trace. This severely cripples debugging during live outages.
**Recommendation:** Use distinct exception classes. Log all unknown exceptions as `logger.error(..., exc_info=True)` before returning HTTP responses.
**Priority:** 🟠 High

---

## 9. Migration Health

**Observation:** Ignored Migration Failures
**Evidence:** `main.py`'s lifespan hook catches generic `OperationalError` when trying to seed demo data and logs: `Demo seeding skipped — database tables not ready`. 
**Production Risk:** If the DB credentials are wrong, or the database is down, this masks a critical infrastructure failure as a simple "tables not ready" warning, allowing the application to boot into a broken state.
**Recommendation:** Tighten exception handling. Ensure Alembic migrations are executed automatically during CI/CD rather than relying on application-boot schema generation. (Also note: `TECHNICAL_DEBT.md` verifies that ENUM modifications are actively blocking Safety schema migrations).
**Priority:** 🟡 Medium

---

## 10. Production Readiness

**Observation:** Startup Configuration and Security
**Evidence:** `main.py` correctly wires `CORSMiddleware` reading from `settings.BACKEND_CORS_ORIGINS`, and implements `slowapi` for rate-limiting via `get_remote_address`. Lifespan context managers are modern and correct.
**Production Risk:** N/A. These are highly robust security defaults.
**Recommendation:** Continue enforcing environment-based configuration validation via Pydantic (`app/core/config.py`).
**Priority:** 🟢 Low
