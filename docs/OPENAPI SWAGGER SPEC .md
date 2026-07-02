# OPENAPI_SWAGGER_SPEC.md

> Project: ConstructPulse
> Version: 2.0
> Status: Production Ready
> Document Type: OpenAPI Specification
> Target Framework: FastAPI
> OpenAPI Version: 3.1
> API Style: REST
> Authentication: JWT + Refresh Token
> Response Format: JSON
> Last Updated: July 2026

---

# 1. Introduction

## 1.1 Purpose

The OpenAPI Specification defines every REST API exposed by the ConstructPulse platform.

It serves as the official contract between frontend applications, backend services, third-party integrations, and AI-assisted development tools.

The specification standardizes request structures, response models, authentication, validation, error handling, pagination, filtering, and versioning across the platform.

This document is implementation-ready and should be used to generate Swagger UI, client SDKs, backend route definitions, and API documentation.

---

# 1.2 Objectives

The API specification aims to:

- Standardize all endpoints.
- Ensure frontend/backend consistency.
- Simplify API development.
- Enable automatic SDK generation.
- Support AI-assisted backend implementation.
- Improve maintainability.
- Enable third-party integrations.
- Support future API versioning.

---

# 1.3 API Design Principles

ConstructPulse APIs follow these principles:

Resource-Oriented

↓

Predictable

↓

RESTful

↓

Secure

↓

Consistent

↓

Versioned

↓

Scalable

↓

Developer Friendly

All endpoints follow common naming conventions and response structures.

---

# 1.4 Base URL

Production

/api/v1

Development

http://localhost:8000/api/v1

Future versions will use:

/api/v2

without affecting existing integrations.

---

# 1.5 API Architecture

Client

↓

Authentication

↓

Permission Validation

↓

Business Logic

↓

Database

↓

Response Builder

↓

JSON Response

Every request passes through authentication, authorization, validation, and audit middleware before reaching business services.

---

# 1.6 Supported Clients

The API supports:

- Flutter Mobile
- React Web Dashboard
- Future Public API
- AI Services
- Internal Microservices
- Third-Party Integrations

All clients consume the same REST API.

---

# 1.7 Authentication

Authentication uses:

- JWT Access Token
- Refresh Token
- Bearer Authentication

Every protected endpoint requires:

Authorization

Bearer <JWT>

Public endpoints are explicitly documented.

---

# 1.8 API Versioning

Current Version

v1

Future versions

v2

v3

Breaking changes require a new API version.

Minor enhancements remain within the current version.

---

# 1.9 Standard Response Format

Every successful response follows:

{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {},
    "metadata": {},
    "timestamp": ""
}

Every error response follows:

{
    "success": false,
    "message": "Validation failed.",
    "errors": [],
    "timestamp": ""
}

This structure is used consistently across all endpoints.

---

# 1.10 HTTP Status Codes

Supported status codes:

200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

429 Too Many Requests

500 Internal Server Error

503 Service Unavailable

Status code usage must remain consistent.

---

# 1.11 Pagination Standard

Collection endpoints support:

page

page_size

sort

order

search

filter

Standard Response

{
    "items": [],
    "page": 1,
    "page_size": 20,
    "total_items": 320,
    "total_pages": 16
}

---

# 1.12 Filtering

Supported filtering:

- Company
- Project
- Site
- Department
- Contractor
- Status
- Date Range
- Search

Filtering syntax remains consistent across endpoints.

---

# 1.13 Sorting

Supported sorting:

sort=name

sort=created_at

sort=updated_at

sort=status

Order:

asc

desc

---

# 1.14 API Documentation

Every endpoint includes:

- Purpose
- Authentication
- Request Parameters
- Request Body
- Success Response
- Error Responses
- Validation Rules
- Permissions
- Example Requests
- Example Responses

Swagger UI should be automatically generated from this specification.

---

# 1.15 Document Organization

Endpoints are grouped into:

Authentication

↓

Users

↓

Companies

↓

Projects

↓

Sites

↓

Workers

↓

Attendance

↓

Safety

↓

Compliance

↓

Assets

↓

Visitors

↓

Reports

↓

AI

↓

Administration

↓

System

This organization mirrors the business architecture of ConstructPulse.

---

# PART 2 — Authentication API

The Authentication API manages secure access to the ConstructPulse platform using OTP-based passwordless authentication.

Authentication endpoints are responsible for identity verification, session creation, token management, logout, and authenticated user context retrieval.

All authentication endpoints must follow enterprise-grade security practices while minimizing friction for field users.

---

# 2. Authentication API

Authentication Flow

Request OTP

↓

Verify OTP

↓

Generate JWT

↓

Generate Refresh Token

↓

Return User Context

↓

Authenticated Session

↓

Refresh Token (When Required)

↓

Logout

---

# 2.1 POST /auth/request-otp

## Purpose

Generate and send a One-Time Password (OTP) to a registered mobile number.

Authentication

Public

Permissions

None

Request Body

{
    "phone_number": "+919876543210"
}

Validation

- Phone number required
- Valid country code
- Registered user
- Rate limiting enabled

Success Response (200)

{
    "success": true,
    "message": "OTP sent successfully.",
    "data": {
        "expires_in": 300,
        "retry_after": 30
    }
}

Error Responses

400 Invalid Phone Number

404 User Not Found

429 Too Many Requests

Business Rules

- OTP valid for 5 minutes.
- Maximum resend attempts configurable.
- OTP stored securely.
- Previous OTP invalidated.

Audit Events

OTP Requested

Frontend Usage

Login Screen

Related Database Tables

users

otp_requests

---

# 2.2 POST /auth/verify-otp

## Purpose

Verify the submitted OTP and create an authenticated session.

Authentication

Public

Permissions

None

Request Body

{
    "phone_number": "+919876543210",
    "otp": "123456"
}

Validation

- OTP required
- Six digits
- Not expired
- Retry attempts within limit

Success Response (200)

{
    "success": true,
    "message": "Authentication successful.",
    "data": {
        "access_token": "...",
        "refresh_token": "...",
        "expires_in": 3600,
        "user": {},
        "permissions": []
    }
}

Error Responses

400 Invalid OTP

401 OTP Expired

403 Account Disabled

429 Too Many Attempts

Business Rules

- Create JWT.
- Create Refresh Token.
- Initialize session.
- Load company context.
- Load permissions.

Audit Events

User Logged In

Frontend Usage

OTP Verification Screen

Related Database Tables

users

sessions

companies

roles

permissions

---

# 2.3 POST /auth/refresh

## Purpose

Generate a new JWT using a valid refresh token.

Authentication

Refresh Token

Permissions

Authenticated User

Request Body

{
    "refresh_token": "..."
}

Validation

- Refresh token required
- Must be valid
- Must not be revoked

Success Response

{
    "success": true,
    "data": {
        "access_token": "...",
        "expires_in": 3600
    }
}

Error Responses

401 Invalid Refresh Token

403 Session Expired

Business Rules

- Issue new JWT.
- Rotate refresh token (recommended).
- Preserve active session.

Audit Events

Session Refreshed

Frontend Usage

Automatic Background Refresh

Related Database Tables

sessions

---

# 2.4 POST /auth/logout

## Purpose

Terminate the current authenticated session.

Authentication

Bearer JWT

Permissions

Authenticated User

Request Body

{}

Validation

- Valid access token

Success Response

{
    "success": true,
    "message": "Logged out successfully."
}

Business Rules

- Revoke refresh token.
- Invalidate session.
- Clear device session.

Audit Events

User Logged Out

Frontend Usage

Profile Menu

Settings

Related Database Tables

sessions

---

# 2.5 GET /auth/me

## Purpose

Return the authenticated user's profile, permissions, assigned company, assigned projects, and operational context.

Authentication

Bearer JWT

Permissions

Authenticated User

Query Parameters

None

Success Response

{
    "success": true,
    "data": {
        "user": {},
        "company": {},
        "roles": [],
        "permissions": [],
        "assigned_sites": [],
        "assigned_projects": []
    }
}

Business Rules

- Company isolation enforced.
- Permissions resolved dynamically.
- Latest profile returned.

Audit Events

None

Frontend Usage

Application Launch

Home Screen

Profile Screen

Related Database Tables

users

companies

roles

permissions

worker_to_site

---

# 2.6 Authentication Security Rules

The Authentication API enforces:

- JWT Authentication
- Refresh Token Rotation
- OTP Expiration
- Retry Limits
- Rate Limiting
- Session Timeout
- Secure Token Storage
- Company Isolation
- Role Validation
- Audit Logging

Every authenticated request passes through the authentication middleware.

---

# 2.7 Acceptance Criteria

✓ OTP generation works.

✓ OTP verification succeeds.

✓ JWT generated correctly.

✓ Refresh token rotation works.

✓ Logout invalidates session.

✓ Authenticated user context loads correctly.

✓ Security policies enforced.

---

## Developer Checklist

### Backend

- [ ] Request OTP Endpoint
- [ ] Verify OTP Endpoint
- [ ] Refresh Endpoint
- [ ] Logout Endpoint
- [ ] Current User Endpoint
- [ ] JWT Middleware
- [ ] Refresh Token Rotation
- [ ] Rate Limiting

### Frontend

- [ ] Login Repository
- [ ] OTP Screen Integration
- [ ] Token Storage
- [ ] Auto Refresh
- [ ] Logout Flow

### QA

- [ ] OTP Success
- [ ] Invalid OTP
- [ ] Expired OTP
- [ ] Refresh Flow
- [ ] Logout
- [ ] Session Expiry

### AI Coding Agent

Required Modules

- Auth Router
- Auth Service
- OTP Service
- JWT Manager
- Session Repository
- Authentication Middleware
- Refresh Token Manager

---

# PART 3 — User & Company API

The User & Company API manages organizational structures, user accounts, roles, permissions, departments, contractors, and company-level configuration.

These endpoints establish the organizational hierarchy used throughout ConstructPulse and enforce strict tenant isolation across multiple companies.

Every operational resource belongs to a company and every authenticated user operates within an isolated company context.

---

# 3. User & Company API

Organization Created

↓

Users Added

↓

Roles Assigned

↓

Permissions Granted

↓

Departments Created

↓

Contractors Registered

↓

Organization Operational

---

# 3.1 Company Endpoints

## GET /companies

### Purpose

Retrieve companies visible to the authenticated user.

Authentication

Bearer JWT

Permissions

Company Admin

Super Admin

Query Parameters

page

page_size

search

status

sort

Success Response

{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "ABC Construction",
            "status": "ACTIVE",
            "active_projects": 5,
            "active_sites": 18
        }
    ]
}

Business Rules

- Company isolation enforced.
- Company Admin only sees own company.
- Super Admin sees all companies.

Audit Events

Company List Viewed

---

## POST /companies

### Purpose

Create a new company.

Authentication

Bearer JWT

Permissions

Super Admin

Request Body

{
    "name": "ABC Construction",
    "registration_number": "REG123456",
    "address": "...",
    "contact_number": "...",
    "email": "..."
}

Validation

- Company name unique.
- Registration number unique.
- Contact number required.

Success Response

201 Created

Business Rules

- Default roles created automatically.
- Default settings initialized.
- Company workspace provisioned.

Audit Events

Company Created

Related Tables

companies

company_settings

---

## PUT /companies/{company_id}

Purpose

Update company information.

Permissions

Company Admin

Super Admin

Business Rules

- Company name uniqueness maintained.
- Configuration changes versioned.

Audit Events

Company Updated

---

# 3.2 User Endpoints

## GET /users

Purpose

Retrieve users within company scope.

Permissions

Company Admin

HR Manager

Project Manager

Query Parameters

page

page_size

role

status

department

site

search

Success Response

{
    "success": true,
    "data": []
}

Business Rules

- Users limited to company scope.
- Supports pagination and filtering.

---

## POST /users

Purpose

Create a platform user.

Authentication

Bearer JWT

Permissions

Company Admin

Request Body

{
    "full_name": "",
    "phone_number": "",
    "role": "",
    "department_id": 1
}

Validation

- Mobile number unique.
- Role required.
- Department optional.

Business Rules

- User initially inactive.
- OTP invitation sent.
- Audit record created.

Audit Events

User Created

---

## GET /users/{user_id}

Purpose

Retrieve complete user profile.

Displays

- Personal Information
- Assigned Roles
- Permissions
- Assigned Sites
- Assigned Projects
- Status

Business Rules

- Company isolation enforced.

---

## PUT /users/{user_id}

Purpose

Update user information.

Supports

- Role Change
- Department Change
- Status Change
- Contact Details

Audit Events

User Updated

---

## DELETE /users/{user_id}

Purpose

Deactivate user.

Business Rules

- Historical records preserved.
- Attendance retained.
- Audit retained.

---

# 3.3 Role Management

## GET /roles

Returns all available roles.

Default Roles

- Super Admin
- Company Admin
- Project Manager
- Site Manager
- Supervisor
- Safety Officer
- HR Manager
- Worker
- Contractor

---

## POST /roles

Create custom role.

Supports

- Name
- Description
- Permission Set

---

# 3.4 Permission Management

## GET /permissions

Returns complete permission catalog.

Permission Types

- Read
- Create
- Update
- Delete
- Approve
- Export
- Configure

Permissions are grouped by module.

---

## POST /roles/{role_id}/permissions

Assign permissions to role.

Business Rules

- Changes immediately affect authorization.
- Audit required.

---

# 3.5 Department Endpoints

Supported Operations

GET /departments

POST /departments

PUT /departments/{id}

DELETE /departments/{id}

Department Fields

- Name
- Description
- Manager
- Active Status

Departments remain company specific.

---

# 3.6 Contractor Endpoints

Supported Operations

GET /contractors

POST /contractors

PUT /contractors/{id}

DELETE /contractors/{id}

Displays

- Contractor Name
- Company
- Contact
- Assigned Sites
- Workforce Count
- Status

Contractors remain isolated within company boundaries.

---

# 3.7 Search Endpoint

## GET /search

Global organizational search.

Supports

Users

Companies

Departments

Contractors

Sites

Projects

Workers

Assets

Visitors

Search returns only authorized resources.

---

# 3.8 Acceptance Criteria

✓ Company CRUD works.

✓ User CRUD works.

✓ Roles function correctly.

✓ Permissions enforced.

✓ Department management works.

✓ Contractor management works.

✓ Company isolation maintained.

---

## Developer Checklist

### Backend

- [ ] Company Router
- [ ] User Router
- [ ] Role Router
- [ ] Permission Router
- [ ] Department Router
- [ ] Contractor Router
- [ ] Search Service

### Frontend

- [ ] Company Management
- [ ] User Management
- [ ] Role Management
- [ ] Permission Matrix
- [ ] Department Screens
- [ ] Contractor Screens
- [ ] Global Search

### QA

- [ ] Company CRUD
- [ ] User CRUD
- [ ] Permission Validation
- [ ] Search Validation
- [ ] Company Isolation
- [ ] Pagination

### AI Coding Agent

Required Modules

- Company Service
- User Service
- Role Service
- Permission Service
- Department Service
- Contractor Service
- Search Engine

---

# PART 4 — Project & Site API

The Project & Site API manages construction projects, operational sites, site assignments, QR code generation, operational readiness, occupancy monitoring, and project lifecycle management.

Projects define the organizational scope of work while Sites represent the physical operational locations where workforce, attendance, safety, compliance, visitors, and assets are managed.

Every operational event within ConstructPulse is associated with a Project and/or Site.

---

# 4. Project & Site API

Project Created

↓

Site Created

↓

QR Generated

↓

Workers Assigned

↓

Operations Begin

↓

Daily Operations

↓

Project Completed

↓

Site Archived

---

# 4.1 GET /projects

## Purpose

Retrieve all projects accessible to the authenticated user.

Authentication

Bearer JWT

Permissions

Project Manager

Company Admin

Super Admin

Query Parameters

page

page_size

status

company_id

search

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Company isolation enforced.
- Pagination mandatory.
- Soft-deleted projects excluded.

Rate Limit

120 requests/minute

Audit Event

Projects Viewed

Database Tables

projects

companies

---

# 4.2 POST /projects

## Purpose

Create a new construction project.

Authentication

Bearer JWT

Permissions

Company Admin

Super Admin

Request Body

{
    "name": "",
    "company_id": 1,
    "description": "",
    "location": "",
    "planned_start_date": "",
    "planned_end_date": ""
}

Validation

- Name required
- Company required
- Start date < End date

Success Response

201 Created

Business Rules

- Project name unique within company.
- Default project settings created.
- Initial audit log generated.

Rate Limit

20 requests/minute

Idempotency

Supported

Audit Event

Project Created

Database Tables

projects

audit_logs

---

# 4.3 GET /projects/{project_id}

Purpose

Retrieve complete project details.

Returns

- Project Information
- Assigned Sites
- Managers
- Workforce Summary
- Operational Readiness
- Progress Metrics
- Timeline
- AI Summary

Business Rules

Company isolation mandatory.

Audit Event

Project Viewed

---

# 4.4 PUT /projects/{project_id}

Purpose

Update project information.

Supports

- Name
- Description
- Timeline
- Managers
- Status

Business Rules

Completed projects become read-only.

Audit Event

Project Updated

---

# 4.5 DELETE /projects/{project_id}

Purpose

Archive a project.

Business Rules

- Cannot delete active projects.
- Historical data preserved.
- Soft delete only.

Audit Event

Project Archived

---

# 4.6 GET /sites

Purpose

Retrieve operational sites.

Query Parameters

project_id

status

company_id

search

page

page_size

Returns

- Site Details
- Occupancy
- Capacity
- Operational Readiness
- Weather
- Active Workforce

Rate Limit

120 requests/minute

---

# 4.7 POST /sites

Purpose

Create a construction site.

Authentication

Bearer JWT

Permissions

Project Manager

Company Admin

Request Body

{
    "project_id": 1,
    "name": "",
    "capacity": 250,
    "latitude": "",
    "longitude": "",
    "address": ""
}

Validation

- Project required.
- Capacity > 0.
- Coordinates valid.

Business Rules

- QR generated automatically.
- Operational dashboard initialized.
- Default attendance settings created.

Idempotency

Supported

Audit Event

Site Created

Database Tables

sites

site_qr_codes

occupancy_snapshots

---

# 4.8 GET /sites/{site_id}

Purpose

Retrieve complete Site Workspace.

Returns

- Site Information
- Occupancy
- Attendance
- Workers
- Visitors
- Assets
- Safety
- Compliance
- AI Summary

Frontend Usage

Site Workspace

Dashboard

---

# 4.9 PUT /sites/{site_id}

Purpose

Update site configuration.

Supports

- Capacity
- Supervisors
- Address
- Coordinates
- Status

Business Rules

QR remains unchanged unless regenerated.

Audit Event

Site Updated

---

# 4.10 POST /sites/{site_id}/generate-qr

Purpose

Generate a new operational QR code.

Authentication

Bearer JWT

Permissions

Site Manager

Company Admin

Validation

- Site active.
- Existing QR archived.

Returns

{
    "success": true,
    "data": {
        "qr_code": "...",
        "expires": null
    }
}

Business Rules

- Previous QR invalidated.
- Attendance immediately uses new QR.

Idempotency

No

Audit Event

QR Regenerated

---

# 4.11 GET /sites/{site_id}/dashboard

Purpose

Retrieve complete operational dashboard.

Returns

- Occupancy
- Attendance
- Safety
- Compliance
- Assets
- Visitors
- Weather
- AI Recommendations
- Operational Readiness

Frontend Usage

Site Workspace

---

# 4.12 POST /sites/{site_id}/close

Purpose

Close operational site.

Validation

- No active attendance.
- No emergency.
- Closure reason required.

Business Rules

- Site becomes read-only.
- Attendance disabled.
- QR archived.

Audit Event

Site Closed

---

# 4.13 GET /projects/{project_id}/timeline

Purpose

Retrieve project operational timeline.

Displays

- Attendance Events
- Safety Events
- Asset Events
- Visitor Events
- AI Events
- Administrative Changes

Supports

Pagination

Filtering

Export

---

# 4.14 Acceptance Criteria

✓ Project CRUD complete.

✓ Site CRUD complete.

✓ QR generation works.

✓ Site Dashboard loads.

✓ Timeline generated.

✓ Operational readiness calculated.

✓ Company isolation enforced.

---

## Developer Checklist

### Backend

- [ ] Project Router
- [ ] Site Router
- [ ] QR Service
- [ ] Timeline Service
- [ ] Readiness Engine
- [ ] Dashboard Service

### Frontend

- [ ] Project Screens
- [ ] Site Screens
- [ ] Site Workspace
- [ ] QR Generator
- [ ] Timeline
- [ ] Dashboard Widgets

### QA

- [ ] Project CRUD
- [ ] Site CRUD
- [ ] QR Generation
- [ ] Dashboard Validation
- [ ] Timeline
- [ ] Company Isolation

### AI Coding Agent

Required Modules

- Project Service
- Site Service
- Dashboard Service
- Timeline Engine
- QR Generator
- Readiness Engine
- Audit Service

---

# PART 5 — Workforce API

The Workforce API manages the complete lifecycle of workers within the ConstructPulse platform.

Workers are the central operational entities used across attendance, safety, compliance, project assignments, payroll integrations, AI analytics, and reporting.

The Workforce API ensures worker information remains consistent, auditable, secure, and synchronized across all operational modules.

Every worker belongs to a company and may be assigned to multiple projects and sites according to organizational policies.

---

# 5. Workforce API

Worker Registration

↓

Verification

↓

Approval

↓

Assignment

↓

Operational Activities

↓

Transfer

↓

Suspension

↓

Archive

↓

Historical Reporting

---

# 5.1 GET /workers

## Purpose

Retrieve workers accessible to the authenticated user.

Authentication

Bearer JWT

Permissions

HR Manager

Supervisor

Project Manager

Company Admin

Super Admin

Query Parameters

page

page_size

search

company_id

project_id

site_id

department_id

contractor_id

trade

status

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Company isolation enforced.
- Pagination required.
- Supports advanced filtering.

Rate Limit

120 requests/minute

Audit Event

Workers Viewed

Database Tables

workers

worker_to_site

departments

contractors

---

# 5.2 POST /workers

## Purpose

Register a new worker.

Authentication

Bearer JWT

Permissions

HR Manager

Company Admin

Request Body

{
    "full_name": "",
    "phone_number": "",
    "trade": "",
    "department_id": 1,
    "contractor_id": 2,
    "employment_type": "",
    "emergency_contact": {},
    "documents": []
}

Validation

- Name required.
- Mobile number unique.
- Trade required.
- Company context required.

Business Rules

- Worker initially Pending Approval.
- Worker Passport created.
- Audit record generated.
- AI readiness evaluation scheduled.

Rate Limit

30 requests/minute

Idempotency

Supported

Audit Event

Worker Registered

Notification Event

HR Approval Required

Database Tables

workers

worker_documents

audit_logs

notifications

---

# 5.3 GET /workers/{worker_id}

## Purpose

Retrieve complete Worker Workspace.

Returns

- Personal Details
- Employment Details
- Assigned Company
- Assigned Projects
- Assigned Sites
- Attendance Summary
- Compliance Status
- Safety Status
- Documents
- Operational Readiness
- AI Summary
- Timeline

Frontend Usage

Worker Workspace

Worker Profile

Business Rules

Only authorized users may view worker details.

---

# 5.4 PUT /workers/{worker_id}

Purpose

Update worker information.

Supports

- Personal Details
- Employment Information
- Emergency Contact
- Department
- Contractor
- Trade

Business Rules

Critical updates generate audit logs.

Audit Event

Worker Updated

---

# 5.5 POST /workers/{worker_id}/approve

Purpose

Approve worker registration.

Permissions

HR Manager

Company Admin

Validation

- Required documents verified.
- Compliance complete.

Business Rules

- Status becomes ACTIVE.
- Attendance eligibility enabled.
- Notifications sent.

Audit Event

Worker Approved

Notification Event

Worker Activated

---

# 5.6 POST /workers/{worker_id}/reject

Purpose

Reject worker registration.

Validation

Reason required.

Business Rules

- Status becomes REJECTED.
- Comments mandatory.
- Worker notified.

Audit Event

Worker Rejected

---

# 5.7 POST /workers/{worker_id}/assign

Purpose

Assign worker to a project and site.

Request Body

{
    "project_id": 1,
    "site_id": 2,
    "department_id": 3,
    "supervisor_id": 10
}

Business Rules

- Worker must be ACTIVE.
- Site must belong to project.
- Assignment history retained.

Audit Event

Worker Assigned

Notification Event

Supervisor Notified

---

# 5.8 POST /workers/{worker_id}/transfer

Purpose

Transfer worker between sites.

Validation

- Current attendance closed.
- New assignment valid.

Business Rules

- Transfer history immutable.
- Operational context updated immediately.

Audit Event

Worker Transferred

---

# 5.9 POST /workers/{worker_id}/suspend

Purpose

Suspend worker.

Request Body

{
    "reason": "",
    "effective_date": ""
}

Business Rules

- Worker cannot check in.
- Existing attendance preserved.
- Suspension logged.

Audit Event

Worker Suspended

---

# 5.10 POST /workers/{worker_id}/archive

Purpose

Archive worker.

Business Rules

- Historical records retained.
- Login disabled.
- Attendance preserved.
- Compliance retained.

Audit Event

Worker Archived

---

# 5.11 GET /workers/{worker_id}/timeline

Purpose

Retrieve worker operational history.

Returns

- Attendance Events
- Site Transfers
- Compliance Events
- Safety Events
- Training
- Documents
- AI Events

Supports

Pagination

Filtering

Export

---

# 5.12 GET /workers/search

Purpose

Advanced workforce search.

Supports

- Name
- Phone
- Trade
- Department
- Contractor
- Company
- Site
- Status

Returns only authorized workers.

---

# 5.13 Acceptance Criteria

✓ Worker registration succeeds.

✓ Approval workflow complete.

✓ Assignment works.

✓ Transfer works.

✓ Suspension blocks attendance.

✓ Archive preserves history.

✓ Timeline generated correctly.

---

## Developer Checklist

### Backend

- [ ] Worker Router
- [ ] Registration Service
- [ ] Approval Service
- [ ] Assignment Service
- [ ] Transfer Service
- [ ] Timeline Service
- [ ] Search Service

### Frontend

- [ ] Worker List
- [ ] Worker Registration
- [ ] Worker Workspace
- [ ] Assignment Dialog
- [ ] Transfer Dialog
- [ ] Timeline
- [ ] Search

### QA

- [ ] Registration
- [ ] Approval
- [ ] Assignment
- [ ] Transfer
- [ ] Suspension
- [ ] Archive
- [ ] Timeline

### AI Coding Agent

Required Modules

- Worker Router
- Worker Service
- Worker Repository
- Assignment Engine
- Timeline Service
- Notification Engine
- Audit Logger

---

# PART 6 — Attendance API

The Attendance API manages workforce presence across construction sites through secure QR-based check-in and check-out workflows.

Attendance serves as the operational source of truth for workforce presence, occupancy monitoring, emergency mustering, productivity analytics, operational readiness, and future payroll integration.

Every attendance event is immutable, fully auditable, and propagated throughout the ConstructPulse platform.

---

# 6. Attendance API

Worker Eligible

↓

Scan Site QR

↓

Validate Worker

↓

Validate Site

↓

Check-In

↓

Occupancy Updated

↓

Operational Activities

↓

Check-Out

↓

Attendance Closed

↓

Analytics Updated

---

# 6.1 POST /attendance/check-in

## Purpose

Record a worker's check-in at a construction site.

Authentication

Bearer JWT

Permissions

Worker

Supervisor

Site Manager

Request Body

{
    "site_qr_code": "",
    "device_timestamp": "",
    "gps_location": {
        "latitude": "",
        "longitude": ""
    }
}

Validation

- Worker must be ACTIVE.
- Worker assigned to site.
- QR must be valid.
- No existing active attendance.
- Site operational.
- Company isolation enforced.

Business Rules

- Attendance record immutable.
- Occupancy incremented.
- Attendance timeline created.
- Dashboard updated.
- AI event generated.

Rate Limit

60 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Worker Checked In

Notification Event

Supervisor Dashboard Updated

Database Tables

attendances

occupancy_snapshots

attendance_events

---

# 6.2 POST /attendance/check-out

## Purpose

Record worker check-out.

Authentication

Bearer JWT

Permissions

Worker

Supervisor

Request Body

{
    "site_qr_code": "",
    "device_timestamp": ""
}

Validation

- Active attendance exists.
- Same site.
- QR valid.

Business Rules

- Duration calculated.
- Occupancy decremented.
- Attendance finalized.
- AI analytics updated.

Rate Limit

60 requests/minute

Idempotency

Supported

Audit Event

Worker Checked Out

Notification Event

Dashboard Updated

Database Tables

attendances

occupancy_snapshots

---

# 6.3 GET /attendance/today

## Purpose

Retrieve today's attendance.

Query Parameters

site_id

project_id

worker_id

status

page

page_size

Returns

- Worker
- Check-In
- Check-Out
- Duration
- Attendance Status
- Site

Frontend Usage

Attendance Dashboard

Supervisor Workspace

---

# 6.4 GET /attendance/history

Purpose

Retrieve historical attendance.

Supports

- Date Range
- Worker
- Site
- Project
- Status
- Export

Business Rules

Historical attendance immutable.

---

# 6.5 POST /attendance/correct

Purpose

Submit attendance correction request.

Request Body

{
    "attendance_id": "",
    "reason": "",
    "corrected_check_in": "",
    "corrected_check_out": ""
}

Validation

- Reason mandatory.
- Authorized role.
- Attendance exists.

Business Rules

- Original record preserved.
- Correction history maintained.
- Approval workflow supported.

Audit Event

Attendance Corrected

---

# 6.6 GET /occupancy/current

Purpose

Retrieve live site occupancy.

Returns

- Current Workers
- Visitors
- Contractors
- Capacity
- Occupancy %
- Last Updated

Frontend Usage

Site Dashboard

Emergency Dashboard

---

# 6.7 GET /occupancy/history

Purpose

Retrieve occupancy trends.

Supports

Hourly

Daily

Weekly

Monthly

Returns

Occupancy timeline.

AI uses this endpoint for workforce analytics.

---

# 6.8 POST /attendance/sync

Purpose

Synchronize offline attendance records.

Authentication

Bearer JWT

Permissions

Authenticated Worker

Request Body

{
    "attendance_records": []
}

Business Rules

- Duplicate detection.
- Conflict resolution.
- Preserve original timestamps.
- Partial success supported.

Audit Event

Offline Attendance Synchronized

---

# 6.9 POST /attendance/emergency-freeze

Purpose

Freeze attendance changes during an active emergency.

Permissions

Safety Officer

Site Manager

Company Admin

Business Rules

- Check-ins disabled.
- Check-outs restricted based on emergency policy.
- Emergency muster becomes authoritative.

Audit Event

Attendance Frozen

---

# 6.10 GET /attendance/dashboard

Purpose

Retrieve attendance operational dashboard.

Returns

- Active Attendance
- Late Check-Ins
- Missing Check-Outs
- Occupancy
- Attendance Trends
- AI Insights

Frontend Usage

Attendance Workspace

Executive Dashboard

---

# 6.11 Acceptance Criteria

✓ Check-In succeeds.

✓ Check-Out succeeds.

✓ Occupancy accurate.

✓ Offline synchronization works.

✓ Corrections audited.

✓ Emergency freeze enforced.

✓ Dashboard reflects live data.

---

## Developer Checklist

### Backend

- [ ] Attendance Router
- [ ] Check-In Service
- [ ] Check-Out Service
- [ ] Occupancy Engine
- [ ] Offline Sync Engine
- [ ] Correction Workflow
- [ ] Dashboard API

### Frontend

- [ ] QR Scanner
- [ ] Attendance Dashboard
- [ ] Attendance History
- [ ] Occupancy Widget
- [ ] Offline Sync
- [ ] Correction Dialog

### QA

- [ ] Check-In
- [ ] Check-Out
- [ ] Duplicate Prevention
- [ ] Occupancy Accuracy
- [ ] Offline Sync
- [ ] Correction Workflow
- [ ] Emergency Freeze

### AI Coding Agent

Required Modules

- Attendance Router
- Attendance Service
- QR Validation Service
- Occupancy Engine
- Sync Service
- Dashboard Service
- Audit Logger
- Event Publisher

---

# PART 7 — Safety API

The Safety API manages hazards, incidents, near misses, toolbox talks, inspections, emergency operations, emergency mustering, and organizational safety intelligence.

Safety is deeply integrated into attendance, operational readiness, AI recommendations, compliance monitoring, notifications, and executive reporting.

Every safety event is fully auditable and contributes to continuous operational improvement.

The Safety API prioritizes proactive risk reduction over reactive incident management.

---

# 7. Safety API

Hazard Identified

↓

Hazard Reported

↓

Risk Assessment

↓

Corrective Action

↓

Verification

↓

Closure

━━━━━━━━━━━━━━━━━━━━━━

Emergency Declared

↓

Emergency Broadcast

↓

Attendance Frozen

↓

Emergency Muster

↓

Personnel Accounted

↓

Emergency Closed

---

# 7.1 POST /hazards

## Purpose

Create a new hazard report.

Authentication

Bearer JWT

Permissions

Worker

Supervisor

Safety Officer

Site Manager

Request Body

{
    "site_id": 1,
    "hazard_type": "",
    "severity": "LOW|MEDIUM|HIGH|CRITICAL",
    "description": "",
    "location": "",
    "photos": [],
    "reported_at": ""
}

Validation

- Site required.
- Severity required.
- Description required.
- Company isolation enforced.

Business Rules

- Hazard ID generated automatically.
- Status initialized as OPEN.
- AI risk analysis triggered.
- Responsible supervisor notified.

Rate Limit

60 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Hazard Reported

Notification Event

Safety Alert Published

Domain Event

HazardReported

Database Tables

hazards

hazard_photos

audit_logs

notifications

---

# 7.2 GET /hazards

## Purpose

Retrieve hazards visible to the authenticated user.

Query Parameters

page

page_size

site_id

project_id

severity

status

assigned_to

date_range

Returns

- Hazard Details
- Severity
- Status
- Assigned User
- Site
- Created Date

Frontend Usage

Safety Dashboard

Site Workspace

---

# 7.3 PUT /hazards/{hazard_id}

Purpose

Update hazard.

Supports

- Status
- Severity
- Assigned User
- Corrective Actions
- Verification Notes

Business Rules

Closed hazards become read-only.

Audit Event

Hazard Updated

---

# 7.4 POST /hazards/{hazard_id}/close

Purpose

Close verified hazard.

Validation

- Corrective actions completed.
- Verification mandatory.

Business Rules

- Closure timestamp recorded.
- AI safety metrics updated.

Audit Event

Hazard Closed

Domain Event

HazardResolved

---

# 7.5 POST /incidents

Purpose

Report operational incident.

Request Body

{
    "site_id": 1,
    "incident_type": "",
    "severity": "",
    "description": "",
    "affected_workers": [],
    "photos": []
}

Business Rules

- Investigation automatically created.
- Incident reference generated.
- Safety dashboard updated.
- Executive notification if Critical.

Domain Event

IncidentReported

Audit Event

Incident Created

---

# 7.6 GET /incidents

Purpose

Retrieve incidents.

Supports

Filtering

Sorting

Pagination

Date Range

Severity

Status

Investigator

---

# 7.7 POST /inspections

Purpose

Submit safety inspection.

Request Body

{
    "site_id": 1,
    "inspection_template": "",
    "checklist": [],
    "photos": [],
    "remarks": ""
}

Business Rules

- Checklist immutable after submission.
- AI inspection scoring triggered.

Audit Event

Inspection Completed

---

# 7.8 POST /toolbox-talks

Purpose

Create toolbox talk.

Supports

- Topic
- Trainer
- Site
- Date
- Participants
- Attachments

Business Rules

Attendance linked automatically.

Audit Event

Toolbox Talk Conducted

---

# 7.9 POST /emergency/declare

Purpose

Declare emergency.

Permissions

Safety Officer

Site Manager

Company Admin

Request Body

{
    "site_id": 1,
    "emergency_type": "",
    "severity": "",
    "description": ""
}

Business Rules

- Attendance frozen.
- Emergency broadcast initiated.
- Muster automatically launched.
- AI emergency assistant activated.

Rate Limit

10 requests/minute

Audit Event

Emergency Declared

Domain Event

EmergencyDeclared

Subscribers

Attendance

Notifications

Dashboard

AI

Executive Dashboard

Emergency Service

---

# 7.10 GET /emergency/muster

Purpose

Retrieve live emergency muster.

Returns

- Total Personnel
- Accounted Personnel
- Missing Personnel
- Visitors
- Contractors
- Muster Progress

Frontend Usage

Emergency Dashboard

Safety Workspace

---

# 7.11 POST /emergency/resolve

Purpose

Close emergency.

Business Rules

- Attendance restored.
- Emergency timeline completed.
- After-action review created.
- AI incident summary generated.

Audit Event

Emergency Resolved

Domain Event

EmergencyClosed

---

# 7.12 GET /safety/dashboard

Purpose

Retrieve operational safety dashboard.

Returns

- Active Hazards
- Incidents
- Near Misses
- Safety Score
- Inspection Status
- Emergency Status
- AI Risk Analysis

Frontend Usage

Safety Workspace

Executive Dashboard

---

# 7.13 Acceptance Criteria

✓ Hazard reporting works.

✓ Incident workflow complete.

✓ Emergency declaration succeeds.

✓ Muster updates live.

✓ Safety dashboard accurate.

✓ AI recommendations generated.

✓ Audit history preserved.

---

## Developer Checklist

### Backend

- [ ] Hazard Router
- [ ] Incident Router
- [ ] Inspection Router
- [ ] Toolbox Talk Router
- [ ] Emergency Router
- [ ] Muster Engine
- [ ] Safety Dashboard

### Frontend

- [ ] Hazard Reporting
- [ ] Incident Screen
- [ ] Inspection Screen
- [ ] Emergency Dashboard
- [ ] Muster Dashboard
- [ ] Safety Workspace

### QA

- [ ] Hazard Workflow
- [ ] Incident Workflow
- [ ] Inspection Workflow
- [ ] Emergency Flow
- [ ] Muster Validation
- [ ] Dashboard Validation

### AI Coding Agent

Required Modules

- Hazard Service
- Incident Service
- Emergency Service
- Muster Engine
- Safety Analytics
- Notification Engine
- Audit Logger
- Event Publisher

---

# PART 8 — Compliance API

The Compliance API manages worker certifications, site inductions, medical clearances, work permits, training records, and regulatory compliance throughout the workforce lifecycle.

Compliance is continuously monitored and directly influences worker eligibility, operational readiness, attendance authorization, project assignments, AI recommendations, and executive reporting.

Every compliance record is versioned, auditable, and securely managed according to organizational policies.

---

# 8. Compliance API

Document Uploaded

↓

Verification

↓

Approval

↓

Assignment

↓

Active Monitoring

↓

Expiry Detection

↓

Renewal Reminder

↓

Renewal

↓

Archive Previous Version

---

# 8.1 GET /compliance

## Purpose

Retrieve compliance records available to the authenticated user.

Authentication

Bearer JWT

Permissions

HR Manager

Safety Officer

Company Admin

Super Admin

Query Parameters

page

page_size

worker_id

site_id

certificate_type

status

expiry_status

search

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Company isolation enforced.
- Supports filtering and pagination.
- Expired records highlighted.

Rate Limit

120 requests/minute

Audit Event

Compliance Records Viewed

Database Tables

worker_documents

worker_certifications

medical_clearances

permits

---

# 8.2 POST /compliance/certificates

## Purpose

Upload a worker certification.

Authentication

Bearer JWT

Permissions

HR Manager

Company Admin

Request Body

{
    "worker_id": 101,
    "certificate_type": "",
    "certificate_number": "",
    "issue_date": "",
    "expiry_date": "",
    "document": "",
    "issuing_authority": ""
}

Validation

- Worker required.
- Certificate type required.
- Expiry date required.
- Document required.

Business Rules

- Previous version retained.
- Compliance score recalculated.
- AI renewal schedule generated.

Rate Limit

30 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Certificate Uploaded

Notification Event

Compliance Updated

Domain Event

CertificateUploaded

Database Tables

worker_certifications

worker_documents

audit_logs

---

# 8.3 GET /compliance/certificates/{certificate_id}

Purpose

Retrieve certificate details.

Returns

- Certificate Information
- Worker
- Status
- Expiry
- Issuing Authority
- Document Metadata
- Renewal History

Frontend Usage

Worker Workspace

Compliance Workspace

---

# 8.4 PUT /compliance/certificates/{certificate_id}

Purpose

Update certificate metadata.

Supports

- Expiry Date
- Issuing Authority
- Notes

Business Rules

Certificate file remains immutable after approval.

Audit Event

Certificate Updated

---

# 8.5 POST /inductions

Purpose

Record worker induction.

Request Body

{
    "worker_id": 101,
    "site_id": 5,
    "induction_type": "",
    "completed_at": "",
    "expiry_date": ""
}

Business Rules

- Worker becomes eligible for site after successful induction.
- Site-specific induction supported.

Domain Event

InductionCompleted

Audit Event

Worker Inducted

---

# 8.6 POST /medical-clearance

Purpose

Record medical fitness clearance.

Request Body

{
    "worker_id": 101,
    "status": "FIT",
    "expiry_date": "",
    "restrictions": ""
}

Validation

- Authorized medical reviewer required.
- Expiry date mandatory.

Business Rules

- Medical restrictions affect assignment eligibility.
- Sensitive medical information protected by role permissions.

Audit Event

Medical Clearance Updated

---

# 8.7 POST /permits

Purpose

Create operational work permit.

Supported Permit Types

- Work at Height
- Hot Work
- Confined Space
- Excavation
- Crane Operations
- Electrical Isolation
- Custom Permit

Business Rules

- Permit linked to worker and site.
- Expiry monitored automatically.
- AI risk analysis updated.

Domain Event

PermitIssued

---

# 8.8 GET /compliance/dashboard

Purpose

Retrieve compliance dashboard.

Returns

- Compliance Score
- Expiring Certificates
- Expired Certificates
- Medical Status
- Permit Status
- Induction Status
- AI Recommendations

Frontend Usage

Compliance Workspace

Executive Dashboard

---

# 8.9 GET /compliance/expiring

Purpose

Retrieve records approaching expiry.

Query Parameters

days_remaining

Default

30 Days

Returns

- Worker
- Certificate
- Expiry Date
- Priority
- AI Recommendation

Business Rules

Results sorted by business risk.

---

# 8.10 POST /compliance/renew

Purpose

Renew compliance record.

Request Body

{
    "compliance_id": 501,
    "new_document": "",
    "new_expiry_date": ""
}

Business Rules

- Previous record archived.
- New version created.
- Eligibility recalculated.
- Notifications published.

Audit Event

Compliance Renewed

Domain Event

ComplianceRenewed

---

# 8.11 GET /workers/{worker_id}/eligibility

Purpose

Retrieve worker operational eligibility.

Returns

- Overall Eligibility
- Compliance Score
- Missing Requirements
- Expired Documents
- Active Restrictions
- AI Recommendations

Frontend Usage

Worker Workspace

Assignment Dialog

Attendance Validation

---

# 8.12 Acceptance Criteria

✓ Certificate upload succeeds.

✓ Medical clearance recorded.

✓ Site inductions managed.

✓ Permit lifecycle complete.

✓ Renewal workflow functions.

✓ Eligibility calculated correctly.

✓ Dashboard reflects current compliance.

---

## Developer Checklist

### Backend

- [ ] Compliance Router
- [ ] Certificate Service
- [ ] Induction Service
- [ ] Medical Clearance Service
- [ ] Permit Service
- [ ] Eligibility Engine
- [ ] Compliance Dashboard

### Frontend

- [ ] Compliance Workspace
- [ ] Certificate Upload
- [ ] Induction Screen
- [ ] Medical Clearance Screen
- [ ] Permit Management
- [ ] Eligibility Widget
- [ ] Compliance Dashboard

### QA

- [ ] Certificate Upload
- [ ] Induction Workflow
- [ ] Medical Clearance
- [ ] Permit Lifecycle
- [ ] Eligibility Validation
- [ ] Dashboard Validation
- [ ] Renewal Workflow

### AI Coding Agent

Required Modules

- Compliance Router
- Certificate Service
- Eligibility Engine
- Permit Service
- Induction Service
- Medical Service
- Notification Engine
- Audit Logger

---

# PART 9 — Asset & Equipment API

The Asset & Equipment API manages construction equipment, machinery, tools, vehicles, and operational resources throughout their lifecycle.

Assets are continuously monitored to maximize utilization, improve operational readiness, reduce downtime, ensure maintenance compliance, and support predictive analytics.

Every asset event contributes to project execution, workforce productivity, safety monitoring, AI recommendations, and executive reporting.

Assets are treated as operational entities rather than inventory records.

---

# 9. Asset & Equipment API

Asset Registered

↓

Inspection

↓

Assignment

↓

Operational Use

↓

Maintenance

↓

Repair

↓

Return To Service

↓

Retirement

↓

Historical Analytics

---

# 9.1 GET /assets

## Purpose

Retrieve assets accessible to the authenticated user.

Authentication

Bearer JWT

Permissions

Supervisor

Project Manager

Site Manager

Company Admin

Super Admin

Query Parameters

page

page_size

site_id

project_id

asset_type

status

availability

search

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Company isolation enforced.
- Supports filtering.
- Pagination required.

Rate Limit

120 requests/minute

Audit Event

Assets Viewed

Database Tables

assets

asset_assignments

asset_categories

---

# 9.2 POST /assets

## Purpose

Register a new operational asset.

Authentication

Bearer JWT

Permissions

Company Admin

Project Manager

Request Body

{
    "asset_name": "",
    "asset_type": "",
    "serial_number": "",
    "manufacturer": "",
    "purchase_date": "",
    "company_id": 1,
    "site_id": 2
}

Validation

- Asset name required.
- Asset type required.
- Serial number unique.
- Company required.

Business Rules

- Asset ID generated.
- QR generated automatically.
- Asset status initialized as AVAILABLE.
- Operational timeline created.

Rate Limit

20 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Asset Registered

Notification Event

Asset Available

Domain Event

AssetRegistered

Database Tables

assets

asset_qr_codes

audit_logs

---

# 9.3 GET /assets/{asset_id}

Purpose

Retrieve Asset Workspace.

Returns

- Asset Details
- Current Assignment
- Site
- Maintenance Status
- Inspection History
- Utilization Metrics
- Operational Timeline
- AI Summary

Frontend Usage

Asset Workspace

Asset Dashboard

---

# 9.4 PUT /assets/{asset_id}

Purpose

Update asset information.

Supports

- Name
- Status
- Site
- Notes
- Manufacturer
- Specifications

Business Rules

Critical changes generate audit logs.

Audit Event

Asset Updated

---

# 9.5 POST /assets/{asset_id}/assign

Purpose

Assign asset.

Request Body

{
    "site_id": 1,
    "worker_id": 101,
    "expected_return": ""
}

Validation

- Asset available.
- Worker active.
- Site operational.

Business Rules

- Previous assignment closed.
- Timeline updated.
- Dashboard updated.

Audit Event

Asset Assigned

Domain Event

AssetAssigned

---

# 9.6 POST /assets/{asset_id}/inspection

Purpose

Record inspection.

Request Body

{
    "inspection_type": "",
    "checklist": [],
    "photos": [],
    "remarks": ""
}

Business Rules

- Inspection immutable.
- Failed inspection creates maintenance recommendation.

Audit Event

Inspection Completed

Domain Event

AssetInspected

---

# 9.7 POST /assets/{asset_id}/maintenance

Purpose

Create maintenance activity.

Request Body

{
    "maintenance_type": "",
    "priority": "",
    "scheduled_date": ""
}

Business Rules

- Asset unavailable during maintenance.
- Operational readiness recalculated.

Audit Event

Maintenance Scheduled

Domain Event

MaintenanceScheduled

---

# 9.8 POST /assets/{asset_id}/breakdown

Purpose

Report equipment breakdown.

Validation

- Asset active.
- Breakdown description required.

Business Rules

- Asset status becomes OUT_OF_SERVICE.
- AI maintenance analysis triggered.
- Supervisor notified.

Audit Event

Asset Breakdown Reported

Domain Event

AssetBreakdownReported

---

# 9.9 POST /assets/{asset_id}/return

Purpose

Return asset to operational service.

Business Rules

- Maintenance completed.
- Inspection passed.
- Status updated to AVAILABLE.

Audit Event

Asset Returned To Service

Domain Event

AssetReturned

---

# 9.10 POST /assets/{asset_id}/retire

Purpose

Retire operational asset.

Business Rules

- Historical records retained.
- Asset becomes read-only.
- QR archived.

Audit Event

Asset Retired

Domain Event

AssetRetired

---

# 9.11 GET /assets/dashboard

Purpose

Retrieve Asset Operations Dashboard.

Returns

- Available Assets
- Assigned Assets
- Under Maintenance
- Out Of Service
- Upcoming Maintenance
- Utilization Rate
- AI Recommendations

Frontend Usage

Asset Workspace

Executive Dashboard

---

# 9.12 GET /assets/{asset_id}/timeline

Purpose

Retrieve complete asset lifecycle.

Returns

- Assignments
- Inspections
- Maintenance
- Repairs
- Breakdowns
- Transfers
- AI Events

Supports

Pagination

Filtering

Export

---

# 9.13 Acceptance Criteria

✓ Asset registration succeeds.

✓ Assignment workflow complete.

✓ Inspection workflow functions.

✓ Maintenance lifecycle complete.

✓ Breakdown reporting works.

✓ Dashboard updates correctly.

✓ Operational timeline preserved.

---

## Developer Checklist

### Backend

- [ ] Asset Router
- [ ] Assignment Service
- [ ] Inspection Service
- [ ] Maintenance Service
- [ ] Breakdown Service
- [ ] Asset Dashboard
- [ ] Timeline Service

### Frontend

- [ ] Asset Workspace
- [ ] Asset Registration
- [ ] Assignment Screen
- [ ] Inspection Screen
- [ ] Maintenance Screen
- [ ] Dashboard
- [ ] Timeline

### QA

- [ ] Registration
- [ ] Assignment
- [ ] Inspection
- [ ] Maintenance
- [ ] Breakdown
- [ ] Dashboard
- [ ] Timeline

### AI Coding Agent

Required Modules

- Asset Router
- Asset Service
- Maintenance Engine
- Inspection Service
- Assignment Service
- Dashboard Service
- Event Publisher
- Audit Logger

---

# PART 10 — Visitor API

The Visitor API manages the complete lifecycle of visitors entering and exiting construction sites, including registration, approvals, digital visitor passes, QR-based check-in/check-out, occupancy tracking, host notifications, and emergency accountability.

Visitors include clients, consultants, auditors, inspectors, vendors, delivery personnel, and temporary personnel.

Every visitor interaction contributes to site security, operational awareness, emergency mustering, AI analytics, and compliance reporting.

---

# 10. Visitor API

Visitor Registered

↓

Approval

↓

Visitor Pass Generated

↓

QR Check-In

↓

Site Access

↓

Visit Monitoring

↓

QR Check-Out

↓

Visit Archived

↓

Historical Analytics

---

# 10.1 GET /visitors

## Purpose

Retrieve visitors accessible to the authenticated user.

Authentication

Bearer JWT

Permissions

Reception

Supervisor

Site Manager

Company Admin

Super Admin

Query Parameters

page

page_size

site_id

project_id

host_id

status

visit_date

search

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Company isolation enforced.
- Pagination supported.
- Filtering supported.

Rate Limit

120 requests/minute

Audit Event

Visitors Viewed

Database Tables

visitors

visitor_passes

visitor_visits

---

# 10.2 POST /visitors

## Purpose

Register a visitor.

Authentication

Bearer JWT

Permissions

Reception

Supervisor

Site Manager

Request Body

{
    "full_name": "",
    "organization": "",
    "phone_number": "",
    "email": "",
    "host_id": 21,
    "site_id": 5,
    "purpose": "",
    "visit_date": "",
    "government_id": ""
}

Validation

- Name required.
- Host required.
- Site required.
- Visit date required.

Business Rules

- Visitor status = PENDING_APPROVAL.
- Visit reference generated.
- Host notified.

Rate Limit

30 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Visitor Registered

Notification Event

Host Approval Requested

Domain Event

VisitorRegistered

Database Tables

visitors

visitor_visits

notifications

---

# 10.3 POST /visitors/{visitor_id}/approve

Purpose

Approve visitor.

Permissions

Supervisor

Site Manager

Company Admin

Business Rules

- Digital visitor pass generated.
- QR generated automatically.
- Host notified.

Audit Event

Visitor Approved

Domain Event

VisitorApproved

---

# 10.4 GET /visitors/{visitor_id}

Purpose

Retrieve Visitor Workspace.

Returns

- Visitor Details
- Organization
- Host
- Site
- Visit History
- Current Status
- Digital Pass
- Timeline

Frontend Usage

Visitor Workspace

Reception Dashboard

---

# 10.5 POST /visitors/check-in

Purpose

Check visitor into site.

Request Body

{
    "visitor_qr": "",
    "device_timestamp": ""
}

Validation

- Visitor approved.
- Visit date valid.
- QR valid.
- No active visit.

Business Rules

- Occupancy updated.
- Host notified.
- Emergency roster updated.

Audit Event

Visitor Checked In

Domain Event

VisitorCheckedIn

---

# 10.6 POST /visitors/check-out

Purpose

Record visitor departure.

Validation

- Active visit exists.

Business Rules

- Visit duration calculated.
- Occupancy updated.
- Timeline completed.

Audit Event

Visitor Checked Out

Domain Event

VisitorCheckedOut

---

# 10.7 GET /visitors/dashboard

Purpose

Retrieve Visitor Operations Dashboard.

Returns

- Active Visitors
- Pending Approvals
- Today's Visits
- Expected Visitors
- Occupancy
- AI Visitor Insights

Frontend Usage

Reception Workspace

Executive Dashboard

---

# 10.8 GET /visitors/{visitor_id}/timeline

Purpose

Retrieve complete visitor history.

Returns

- Registrations
- Approvals
- Check-Ins
- Check-Outs
- Host Changes
- AI Events

Supports

Pagination

Filtering

Export

---

# 10.9 POST /visitors/{visitor_id}/cancel

Purpose

Cancel scheduled visit.

Business Rules

- Active visits cannot be cancelled.
- Host notified.
- Audit generated.

Audit Event

Visitor Cancelled

Domain Event

VisitorCancelled

---

# 10.10 GET /visitors/emergency

Purpose

Retrieve visitors during emergency.

Returns

- Visitors On Site
- Accounted Visitors
- Missing Visitors
- Hosts
- Muster Status

Frontend Usage

Emergency Dashboard

Safety Workspace

---

# 10.11 Acceptance Criteria

✓ Visitor registration succeeds.

✓ Approval workflow complete.

✓ Visitor pass generated.

✓ Check-in/check-out works.

✓ Occupancy updates correctly.

✓ Emergency roster accurate.

✓ Timeline preserved.

---

## Developer Checklist

### Backend

- [ ] Visitor Router
- [ ] Visitor Registration Service
- [ ] Approval Service
- [ ] Visitor Pass Service
- [ ] Check-In Service
- [ ] Dashboard Service
- [ ] Timeline Service

### Frontend

- [ ] Visitor Registration
- [ ] Approval Screen
- [ ] Visitor Workspace
- [ ] Visitor Dashboard
- [ ] QR Check-In
- [ ] Visitor Timeline

### QA

- [ ] Registration
- [ ] Approval
- [ ] Check-In
- [ ] Check-Out
- [ ] Dashboard
- [ ] Emergency Validation
- [ ] Timeline

### AI Coding Agent

Required Modules

- Visitor Router
- Visitor Service
- Visitor Pass Generator
- Dashboard Service
- Timeline Service
- Notification Engine
- Audit Logger
- Event Publisher

---

# PART 11 — Reports & Analytics API

The Reports & Analytics API transforms operational data into actionable business intelligence by aggregating information across workforce, attendance, projects, sites, safety, compliance, assets, visitors, and AI-generated insights.

Rather than querying operational services directly, reporting consumes normalized reporting datasets optimized for analytics, visualization, exports, executive dashboards, and scheduled reporting.

Reports support operational decision-making, regulatory compliance, executive oversight, and AI-assisted forecasting.

---

# 11. Reports & Analytics API

Operational Events

↓

Reporting Pipeline

↓

Data Aggregation

↓

Analytics Engine

↓

Dashboard Generation

↓

AI Analysis

↓

Export

↓

Distribution

↓

Historical Archive

---

# 11.1 GET /reports

## Purpose

Retrieve available reports.

Authentication

Bearer JWT

Permissions

Supervisor

Project Manager

Company Admin

Executive

Super Admin

Query Parameters

page

page_size

category

report_type

site_id

project_id

created_by

search

sort

order

Success Response

{
    "success": true,
    "data": [],
    "metadata": {}
}

Business Rules

- Reports scoped by company.
- Pagination supported.
- Historical reports retained.

Rate Limit

120 requests/minute

Audit Event

Reports Viewed

Database Tables

reports

report_templates

---

# 11.2 POST /reports/generate

## Purpose

Generate an operational report.

Authentication

Bearer JWT

Permissions

Authorized Reporting Roles

Request Body

{
    "report_type": "ATTENDANCE",
    "date_range": {
        "from": "",
        "to": ""
    },
    "filters": {
        "site_ids": [],
        "project_ids": [],
        "departments": []
    },
    "export_format": "PDF"
}

Validation

- Report type required.
- Date range required.
- Export format valid.

Business Rules

- Report generated asynchronously for large datasets.
- Report version stored.
- AI summary generated automatically.

Rate Limit

20 requests/minute

Idempotency

Supported

Headers

Idempotency-Key

Audit Event

Report Generated

Domain Event

ReportGenerated

Database Tables

reports

report_jobs

report_exports

---

# 11.3 GET /reports/{report_id}

Purpose

Retrieve generated report.

Returns

- Metadata
- Report Status
- Download Information
- AI Summary
- Filters Used
- Generated By
- Generated At

Frontend Usage

Reports Workspace

Executive Dashboard

---

# 11.4 POST /reports/export

Purpose

Export report.

Supported Formats

- PDF
- Excel
- CSV

Business Rules

- Export logged.
- Watermark optional.
- Timestamp embedded.
- Company branding applied.

Audit Event

Report Exported

---

# 11.5 GET /analytics/dashboard

Purpose

Retrieve operational dashboard.

Returns

- Workforce KPIs
- Attendance KPIs
- Safety KPIs
- Compliance KPIs
- Asset KPIs
- Visitor KPIs
- Operational Readiness
- AI Insights

Frontend Usage

Executive Dashboard

Company Dashboard

---

# 11.6 GET /analytics/trends

Purpose

Retrieve operational trends.

Supports

Daily

Weekly

Monthly

Quarterly

Yearly

Returns

Trend datasets optimized for visualization.

---

# 11.7 GET /analytics/forecast

Purpose

Retrieve predictive analytics.

Returns

- Workforce Forecast
- Attendance Forecast
- Compliance Risk
- Maintenance Forecast
- Safety Risk
- Capacity Forecast

Business Rules

Generated by AI Forecast Engine.

Domain Event

ForecastGenerated

---

# 11.8 GET /reports/templates

Purpose

Retrieve report templates.

Supports

- Attendance
- Workforce
- Safety
- Compliance
- Assets
- Visitors
- Executive

Custom templates supported.

---

# 11.9 POST /reports/schedule

Purpose

Schedule recurring report generation.

Request Body

{
    "template_id": 1,
    "frequency": "WEEKLY",
    "recipients": [],
    "export_format": "PDF"
}

Business Rules

- Scheduled jobs managed by background worker.
- Delivery history retained.

Audit Event

Report Scheduled

---

# 11.10 GET /analytics/ai-insights

Purpose

Retrieve AI-generated operational insights.

Returns

- Executive Summary
- Operational Risks
- Productivity Trends
- Safety Trends
- Compliance Gaps
- Recommended Actions

Frontend Usage

AI Workspace

Executive Dashboard

---

# 11.11 Acceptance Criteria

✓ Reports generated successfully.

✓ Dashboard data accurate.

✓ Analytics update correctly.

✓ Exports function.

✓ Scheduled reports execute.

✓ AI insights generated.

✓ Historical reports retained.

---

## Developer Checklist

### Backend

- [ ] Reports Router
- [ ] Analytics Router
- [ ] Report Generation Engine
- [ ] Export Service
- [ ] Scheduler
- [ ] AI Insights Service
- [ ] Dashboard Aggregator

### Frontend

- [ ] Reports Workspace
- [ ] Dashboard Widgets
- [ ] Report Builder
- [ ] Export Dialog
- [ ] Trend Charts
- [ ] Scheduled Reports UI
- [ ] AI Insights Panel

### QA

- [ ] Report Generation
- [ ] Export Validation
- [ ] Dashboard Accuracy
- [ ] Scheduled Reports
- [ ] AI Insights
- [ ] Trend Analytics
- [ ] Performance Testing

### AI Coding Agent

Required Modules

- Reports Router
- Analytics Service
- Report Generator
- Dashboard Aggregator
- Export Service
- Forecast Engine
- Scheduler
- Audit Logger

---

# PART 12 — AI API

The AI API provides the intelligence layer of ConstructPulse by delivering contextual recommendations, operational insights, conversational assistance, predictive analytics, report generation, and decision support across every module.

The AI API is not a direct interface to a Large Language Model.

Instead, it exposes a secure AI Gateway responsible for context building, permission enforcement, prompt orchestration, response validation, conversation history, audit logging, and AI analytics.

Every AI response must be explainable, context-aware, permission-aware, and fully auditable.

---

# 12. AI API

User Request

↓

AI Gateway

↓

Permission Validation

↓

Context Builder

↓

Prompt Builder

↓

AI Provider

↓

Response Validator

↓

Business Rules

↓

Audit

↓

Response Returned

---

# 12.1 POST /ai/chat

## Purpose

Process natural language operational queries.

Authentication

Bearer JWT

Permissions

Authenticated User

Request Body

{
    "message": "How many workers are currently at Airport Expansion Site?",
    "conversation_id": "",
    "context": {
        "site_id": 12,
        "project_id": 4
    }
}

Validation

- User authenticated.
- Message required.
- Company isolation enforced.
- Conversation context validated.

Business Rules

- AI only accesses authorized data.
- Context automatically enriched.
- Conversation history preserved.
- Response validated before delivery.

Rate Limit

60 requests/minute

Idempotency

Not Required

Audit Event

AI Conversation Started

Domain Event

AIChatCompleted

Database Tables

ai_conversations

ai_messages

audit_logs

---

# 12.2 GET /ai/recommendations

## Purpose

Retrieve personalized AI recommendations.

Authentication

Bearer JWT

Permissions

Authenticated User

Query Parameters

site_id

project_id

priority

category

Returns

- Recommendation
- Priority
- Confidence Score
- Business Impact
- Supporting Evidence
- Suggested Action

Business Rules

Recommendations filtered by user permissions.

Frontend Usage

Home Dashboard

Site Workspace

Executive Dashboard

---

# 12.3 GET /ai/morning-briefing

Purpose

Generate daily operational briefing.

Returns

- Workforce Summary
- Attendance Overview
- Safety Alerts
- Compliance Alerts
- Weather
- Asset Status
- Operational Readiness
- Today's Priorities

Business Rules

Briefing personalized for every user.

Domain Event

MorningBriefingGenerated

---

# 12.4 GET /ai/insights

Purpose

Retrieve operational insights.

Supports

- Workforce
- Attendance
- Safety
- Compliance
- Assets
- Visitors
- Projects

Returns

AI-generated summaries and recommendations.

---

# 12.5 POST /ai/report

Purpose

Generate AI-powered report.

Request Body

{
    "report_type": "EXECUTIVE",
    "site_id": 10,
    "date_range": {}
}

Business Rules

- AI summary included.
- Recommendations generated.
- Supporting evidence attached.

Audit Event

AI Report Generated

---

# 12.6 GET /ai/history

Purpose

Retrieve AI conversation history.

Returns

- Conversations
- Messages
- Timestamps
- AI Responses
- Feedback

Business Rules

Users only access their own conversations.

---

# 12.7 POST /ai/feedback

Purpose

Collect AI response feedback.

Request Body

{
    "conversation_id": "",
    "rating": 5,
    "feedback": "Helpful recommendation."
}

Business Rules

Feedback used for prompt optimization.

Audit Event

AI Feedback Submitted

---

# 12.8 GET /ai/forecast

Purpose

Retrieve predictive operational forecasts.

Returns

- Workforce Forecast
- Attendance Forecast
- Compliance Risk
- Maintenance Forecast
- Project Delay Risk
- Capacity Forecast

Business Rules

Forecasts generated using operational data and AI models.

Domain Event

ForecastGenerated

---

# 12.9 POST /ai/summarize

Purpose

Generate AI summaries.

Supported Inputs

- Attendance
- Safety
- Compliance
- Site Activity
- Project Activity
- Reports

Returns

- Executive Summary
- Key Findings
- Risks
- Recommendations

Frontend Usage

Executive Workspace

Reports

---

# 12.10 GET /ai/providers

Purpose

Retrieve configured AI providers.

Returns

- Provider Name
- Status
- Supported Models
- Default Model

Permissions

Company Admin

Super Admin

---

# 12.11 AI Gateway Responsibilities

The AI Gateway manages:

- Authentication
- Authorization
- Context Building
- Prompt Construction
- Model Selection
- Response Validation
- Safety Filtering
- Conversation Logging
- Audit Logging
- Metrics Collection

No frontend communicates directly with an AI provider.

---

# 12.12 Acceptance Criteria

✓ Chat responses generated.

✓ Recommendations personalized.

✓ Morning briefing accurate.

✓ AI reports generated.

✓ Forecasts available.

✓ Conversation history preserved.

✓ Permission enforcement validated.

---

## Developer Checklist

### Backend

- [ ] AI Router
- [ ] AI Gateway
- [ ] Context Builder
- [ ] Prompt Builder
- [ ] Provider Manager
- [ ] Response Validator
- [ ] Conversation Service
- [ ] Feedback Service

### Frontend

- [ ] AI Chat
- [ ] AI Side Panel
- [ ] Morning Briefing
- [ ] Recommendations Widget
- [ ] AI History
- [ ] Feedback Dialog

### QA

- [ ] AI Chat
- [ ] Recommendation Accuracy
- [ ] Permission Validation
- [ ] Conversation History
- [ ] Forecast Validation
- [ ] AI Reports
- [ ] Feedback Workflow

### AI Coding Agent

Required Modules

- AI Router
- AI Gateway
- Context Service
- Prompt Service
- Provider Manager
- Conversation Repository
- Recommendation Engine
- Audit Logger

---

# PART 13 — Administration API

The Administration API manages organizational administration, user governance, role-based access control, platform configuration, feature management, audit logging, integrations, and operational policies.

These APIs provide centralized governance for the ConstructPulse platform while enforcing strict multi-tenant isolation, security policies, and auditability.

Administrative APIs are highly privileged and require enhanced authorization, comprehensive audit logging, and strict validation.

---

# 13. Administration API

Organization

↓

Users

↓

Roles

↓

Permissions

↓

Configuration

↓

Integrations

↓

Audit

↓

Platform Governance

---

# 13.1 GET /admin/dashboard

## Purpose

Retrieve platform administration dashboard.

Authentication

Bearer JWT

Permissions

Company Admin

Super Admin

Returns

- Active Users
- Active Companies
- Active Projects
- Operational Health
- License Status
- Feature Flags
- Integration Status
- AI System Status

Business Rules

Dashboard scoped by administrator permissions.

Rate Limit

60 requests/minute

Audit Event

Administration Dashboard Viewed

Database Tables

companies

users

system_settings

feature_flags

---

# 13.2 GET /admin/users

## Purpose

Retrieve platform users.

Query Parameters

page

page_size

company_id

role

status

search

sort

order

Returns

- User Information
- Roles
- Status
- Last Login
- Assigned Company
- Assigned Sites

Business Rules

Company Admin only sees users within their company.

Audit Event

Users Viewed

---

# 13.3 POST /admin/users

Purpose

Create platform user.

Authentication

Bearer JWT

Permissions

Company Admin

Super Admin

Request Body

{
    "full_name": "",
    "phone_number": "",
    "role": "",
    "company_id": 1
}

Validation

- Phone unique.
- Role exists.
- Company exists.

Business Rules

- Invitation sent.
- User inactive until OTP verification.
- Audit generated.

Idempotency

Supported

Audit Event

Administrative User Created

Domain Event

UserProvisioned

---

# 13.4 PUT /admin/users/{user_id}

Purpose

Update user.

Supports

- Role
- Status
- Company
- Contact Details

Business Rules

Role changes invalidate cached permissions.

Audit Event

Administrative User Updated

---

# 13.5 POST /admin/users/{user_id}/disable

Purpose

Disable user.

Business Rules

- Active sessions revoked.
- Login blocked.
- Historical records preserved.

Domain Event

UserDisabled

Audit Event

User Disabled

---

# 13.6 GET /admin/roles

Purpose

Retrieve available roles.

Returns

- Role Name
- Description
- Permissions
- User Count

Supports custom enterprise roles.

---

# 13.7 POST /admin/roles

Purpose

Create custom role.

Request Body

{
    "name": "",
    "description": "",
    "permissions": []
}

Business Rules

- Role names unique within company.
- Permissions validated.

Audit Event

Role Created

---

# 13.8 PUT /admin/roles/{role_id}/permissions

Purpose

Assign permissions.

Business Rules

- Permission cache invalidated.
- Existing sessions refreshed.

Domain Event

PermissionsUpdated

Audit Event

Permissions Modified

---

# 13.9 GET /admin/settings

Purpose

Retrieve platform settings.

Returns

- Attendance Rules
- QR Settings
- Session Configuration
- Offline Configuration
- AI Settings
- Notification Settings

Frontend Usage

Administration Workspace

---

# 13.10 PUT /admin/settings

Purpose

Update platform settings.

Business Rules

- Version history maintained.
- Sensitive settings require confirmation.
- Changes propagated safely.

Audit Event

Settings Updated

---

# 13.11 GET /admin/audit

Purpose

Retrieve audit logs.

Supports

- Date Range
- User
- Module
- Action
- Entity
- Severity

Returns

Immutable audit history.

---

# 13.12 GET /admin/integrations

Purpose

Retrieve configured integrations.

Supported Integrations

- AI Providers
- SMS Gateway
- Email Gateway
- ERP Systems
- Payroll Systems
- IoT Devices
- BIM Platforms

Business Rules

Secrets never returned through API.

---

# 13.13 POST /admin/integrations

Purpose

Configure integration.

Business Rules

- Credentials encrypted.
- Connectivity validated.
- Audit recorded.

Domain Event

IntegrationConfigured

---

# 13.14 GET /admin/feature-flags

Purpose

Retrieve feature flags.

Returns

- Feature
- Status
- Company Scope
- Rollout Percentage

Supports gradual feature rollout.

---

# 13.15 Acceptance Criteria

✓ User administration works.

✓ Role management works.

✓ Permissions enforced.

✓ Settings versioned.

✓ Integrations secured.

✓ Audit logs immutable.

✓ Feature flags configurable.

---

## Security Considerations

Administrative APIs enforce:

- Multi-factor authorization (Future)
- JWT validation
- Company isolation
- Permission verification
- Rate limiting
- Audit logging
- Sensitive operation confirmation
- Secret encryption
- Session revocation
- Principle of Least Privilege

Every administrative action must be fully traceable.

---

## Developer Checklist

### Backend

- [ ] Administration Router
- [ ] User Administration Service
- [ ] Role Service
- [ ] Permission Engine
- [ ] Settings Service
- [ ] Audit Service
- [ ] Integration Manager
- [ ] Feature Flag Service

### Frontend

- [ ] Administration Dashboard
- [ ] User Management
- [ ] Role Management
- [ ] Settings Screens
- [ ] Audit Viewer
- [ ] Integration Settings
- [ ] Feature Flag Manager

### QA

- [ ] User Administration
- [ ] Permission Validation
- [ ] Settings Management
- [ ] Audit Verification
- [ ] Integration Security
- [ ] Feature Flags

### AI Coding Agent

Required Modules

- Administration Router
- User Administration Service
- Role Service
- Permission Engine
- Settings Repository
- Audit Logger
- Integration Service
- Feature Flag Manager

---

# PART 14 — System API

The System API provides infrastructure-level services that support the ConstructPulse platform.

Unlike business APIs, System APIs expose platform capabilities including health monitoring, file management, notifications, background processing, telemetry, diagnostics, cache management, and platform versioning.

These APIs are consumed by frontend applications, backend services, administrators, monitoring tools, DevOps pipelines, and future microservices.

System APIs must remain lightweight, secure, highly available, and independently scalable.

---

# 14. System API

Application Starts

↓

Health Validation

↓

Configuration Loaded

↓

Background Services

↓

Notification Engine

↓

File Services

↓

Telemetry

↓

Monitoring

↓

Operational Platform

---

# 14.1 GET /system/health

## Purpose

Retrieve platform health status.

Authentication

Public (Limited)

Bearer JWT (Detailed View)

Permissions

Authenticated Admin (Detailed Metrics)

Returns

{
    "status": "HEALTHY",
    "version": "2.0.0",
    "database": "CONNECTED",
    "cache": "CONNECTED",
    "storage": "CONNECTED",
    "queue": "CONNECTED",
    "uptime_seconds": 86400
}

Business Rules

- Public endpoint exposes only basic health.
- Detailed metrics require authentication.

Rate Limit

300 requests/minute

Audit Event

System Health Viewed

---

# 14.2 GET /system/version

## Purpose

Retrieve application version information.

Returns

- Version
- Build Number
- Release Date
- API Version
- Git Commit (Optional)
- Environment

Frontend Usage

About Screen

Developer Settings

---

# 14.3 POST /system/upload

Purpose

Upload platform files.

Supported Types

- Images
- PDFs
- Certificates
- Safety Documents
- Reports
- Asset Photos
- Visitor Documents

Validation

- File size limits.
- MIME type validation.
- Virus scanning.
- Company isolation.

Business Rules

- Metadata stored.
- Secure storage.
- Signed URL generation (Future).

Audit Event

File Uploaded

Domain Event

FileUploaded

Database Tables

files

file_metadata

---

# 14.4 GET /system/files/{file_id}

Purpose

Retrieve file metadata.

Returns

- File Name
- Type
- Size
- Uploaded By
- Upload Date
- Linked Entity

Business Rules

Access controlled by permissions.

---

# 14.5 GET /system/notifications

Purpose

Retrieve notifications.

Supports

- Pagination
- Read Status
- Category
- Priority

Returns

- Notifications
- AI Alerts
- Safety Alerts
- System Alerts

Frontend Usage

Notification Center

---

# 14.6 POST /system/notifications/read

Purpose

Mark notifications as read.

Business Rules

- User-specific.
- Bulk updates supported.

Audit Event

Notifications Updated

---

# 14.7 GET /system/jobs

Purpose

Retrieve background jobs.

Displays

- Job Status
- Progress
- Created By
- Started At
- Completed At
- Retry Count

Permissions

Company Admin

Super Admin

---

# 14.8 GET /system/cache

Purpose

Retrieve cache status.

Returns

- Cache Health
- Memory Usage
- Hit Ratio
- Active Keys

Permissions

Super Admin

---

# 14.9 POST /system/cache/clear

Purpose

Clear selected cache.

Validation

Administrative confirmation required.

Business Rules

- Cache invalidation logged.
- Distributed cache synchronized.

Audit Event

Cache Cleared

---

# 14.10 GET /system/telemetry

Purpose

Retrieve platform telemetry.

Returns

- API Usage
- Response Times
- Error Rates
- Queue Status
- Background Jobs
- Active Sessions

Frontend Usage

Administration Workspace

Monitoring Dashboard

---

# 14.11 GET /system/logs

Purpose

Retrieve platform logs.

Supports

- Severity
- Date Range
- Module
- Search

Business Rules

Sensitive information redacted.

Permissions

Super Admin

---

# 14.12 GET /system/status

Purpose

Retrieve complete platform operational status.

Returns

- Database Status
- Queue Status
- Cache Status
- AI Provider Status
- SMS Gateway
- Email Gateway
- Storage
- Integration Health

Used by monitoring systems.

---

# 14.13 Acceptance Criteria

✓ Health endpoint available.

✓ File uploads secure.

✓ Notifications managed.

✓ Background jobs monitored.

✓ Cache management functions.

✓ Telemetry available.

✓ Platform diagnostics accurate.

---

## Security Considerations

System APIs enforce:

- Authentication where required.
- Rate limiting.
- Secure file validation.
- Virus scanning.
- Permission validation.
- Secret redaction.
- Audit logging.
- Administrative confirmation.
- Infrastructure isolation.

Infrastructure endpoints should never expose sensitive platform information publicly.

---

## Developer Checklist

### Backend

- [ ] Health Router
- [ ] Upload Service
- [ ] Notification Service
- [ ] Background Job Manager
- [ ] Cache Manager
- [ ] Telemetry Service
- [ ] System Diagnostics

### Frontend

- [ ] Notification Center
- [ ] File Upload Components
- [ ] System Status Screen
- [ ] Monitoring Dashboard
- [ ] Platform Diagnostics

### QA

- [ ] Health Endpoint
- [ ] File Upload Validation
- [ ] Notification Workflow
- [ ] Cache Management
- [ ] Telemetry Accuracy
- [ ] Security Validation

### AI Coding Agent

Required Modules

- System Router
- Health Service
- Upload Service
- Notification Service
- Cache Manager
- Telemetry Engine
- Diagnostics Service
- Audit Logger

---

# PART 15 — Shared Schemas & Common Components

The Shared Schemas & Common Components section defines reusable API contracts used throughout the ConstructPulse platform.

Rather than redefining request models, response structures, error formats, pagination objects, security schemes, enums, and common entities for every endpoint, these components are centralized to ensure consistency, maintainability, and compatibility across all APIs.

Every REST endpoint within ConstructPulse must reuse these shared components wherever applicable.

---

# 15. Shared Components

Shared Components include:

- Request Models
- Response Models
- Error Models
- Pagination Models
- Filtering Models
- Sorting Models
- Authentication Schemes
- Common Headers
- Standard Enums
- Reusable Entity Schemas
- Domain Event Schemas

---

# 15.1 Standard Success Response

All successful endpoints return:

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {},
  "metadata": {},
  "timestamp": "2026-07-02T10:30:00Z"
}
```

Required Fields

- success
- message
- data
- timestamp

Optional

- metadata

---

# 15.2 Standard Error Response

All error responses return:

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "phone_number",
      "code": "INVALID_PHONE",
      "message": "Phone number is invalid."
    }
  ],
  "timestamp": "2026-07-02T10:30:00Z",
  "trace_id": "REQ-123456789"
}
```

Business Rules

- Never expose stack traces.
- Validation errors returned consistently.
- Trace ID included for debugging.

---

# 15.3 Pagination Schema

```json
{
  "page": 1,
  "page_size": 20,
  "total_items": 250,
  "total_pages": 13,
  "has_next": true,
  "has_previous": false
}
```

Used by all collection endpoints.

---

# 15.4 Sorting Schema

Supported Parameters

sort

order

Supported Values

asc

desc

Example

GET /workers?sort=name&order=asc

---

# 15.5 Filtering Schema

Common Filters

- company_id
- project_id
- site_id
- department_id
- contractor_id
- status
- search
- created_after
- created_before

Filtering syntax remains consistent across all APIs.

---

# 15.6 Authentication Scheme

Authentication Type

Bearer JWT

Authorization Header

Authorization: Bearer <JWT>

Refresh Token

Secure HTTP Only Cookie (Recommended)

Public endpoints explicitly documented.

---

# 15.7 Standard Headers

Supported Headers

Authorization

Content-Type

Accept

Idempotency-Key

X-Request-ID

X-Correlation-ID

Accept-Language

Headers standardized across all services.

---

# 15.8 Standard Enums

Worker Status

- PENDING
- ACTIVE
- SUSPENDED
- ARCHIVED

Attendance Status

- CHECKED_IN
- CHECKED_OUT
- MISSED

Project Status

- PLANNING
- ACTIVE
- COMPLETED
- ARCHIVED

Site Status

- ACTIVE
- CLOSED
- MAINTENANCE

Hazard Severity

- LOW
- MEDIUM
- HIGH
- CRITICAL

Notification Priority

- LOW
- NORMAL
- HIGH
- CRITICAL

---

# 15.9 Common Entity Schemas

Reusable entities include:

Company

User

Worker

Project

Site

Attendance

Hazard

Asset

Visitor

Report

Notification

AI Recommendation

Each entity maintains a single canonical schema.

---

# 15.10 Domain Event Schema

Every published domain event follows:

```json
{
  "event_id": "uuid",
  "event_type": "AttendanceCheckedIn",
  "occurred_at": "2026-07-02T10:30:00Z",
  "company_id": 1,
  "entity_id": 501,
  "payload": {}
}
```

Business Rules

- Events immutable.
- Event IDs globally unique.
- Payload versioned.

---

# 15.11 Audit Event Schema

Audit records include:

```json
{
  "user_id": 101,
  "action": "WorkerCreated",
  "entity": "Worker",
  "entity_id": 501,
  "timestamp": "2026-07-02T10:30:00Z",
  "ip_address": "",
  "device": "",
  "metadata": {}
}
```

Audit events are immutable.

---

# 15.12 Security Schemes

Supported Security

- JWT Authentication
- Refresh Tokens
- RBAC
- Company Isolation
- Permission Validation
- Rate Limiting
- Idempotency
- Audit Logging

Future Support

- OAuth2
- SSO
- MFA

---

# 15.13 File Upload Schema

Standard upload response:

```json
{
  "file_id": "",
  "file_name": "",
  "content_type": "",
  "size": 102400,
  "uploaded_at": "",
  "url": ""
}
```

Files remain company isolated.

---

# 15.14 Notification Schema

Notification Model

- ID
- Category
- Title
- Message
- Priority
- Read Status
- Created At
- Related Entity

Used by all notification APIs.

---

# 15.15 AI Response Schema

Every AI response includes:

- Response
- Confidence Score
- Supporting Evidence
- Business Impact
- Suggested Actions
- References
- Timestamp

AI responses should always be explainable.

---

# 15.16 API Versioning

Current Version

v1

Version Header

API-Version

Breaking changes require:

/api/v2

Older versions remain supported according to platform policy.

---

# 15.17 Acceptance Criteria

✓ Shared schemas reused throughout the platform.

✓ Error models standardized.

✓ Pagination consistent.

✓ Authentication unified.

✓ Entity schemas centralized.

✓ Domain events standardized.

✓ OpenAPI components reusable.

---

## Developer Checklist

### Backend

- [ ] Shared Pydantic Models
- [ ] Response Builders
- [ ] Error Handlers
- [ ] Pagination Helpers
- [ ] Authentication Middleware
- [ ] Enum Definitions
- [ ] Event Models

### Frontend

- [ ] Shared API Models
- [ ] Response Parsers
- [ ] Error Components
- [ ] Pagination Components
- [ ] Authentication Helpers

### QA

- [ ] Response Validation
- [ ] Error Validation
- [ ] Schema Compatibility
- [ ] Authentication
- [ ] Pagination
- [ ] Event Validation

### AI Coding Agent

Required Modules

- Shared Schemas
- Base Models
- Response Builder
- Error Handler
- Authentication Models
- Event Models
- Enum Library

---


