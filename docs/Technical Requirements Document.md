# Technical Requirements Document (TRD)

# ConstructPulse
### Enterprise Construction Workforce Management Platform

---

## Document Information

| Field | Value |
|--------|-------|
| Document | Technical Requirements Document |
| Product | ConstructPulse |
| Client | Limelite Construction Ltd. |
| Version | 3.0 |
| Status | Production Planning |
| Prepared By | ConstructPulse Development Team |
| Target Platform | Android / iOS / Web (Future) |
| Backend | FastAPI |
| Frontend | Flutter |
| Database | PostgreSQL |
| Country | New Zealand |

---

# Table of Contents

1. Introduction
2. Technical Goals
3. System Architecture
4. Technology Stack
5. High-Level Architecture
6. Application Architecture
7. Authentication & Authorization
8. Role Based Access Control (RBAC)
9. Company Management
10. Site Management
11. Workforce Management
12. Attendance Engine
13. GPS Validation
14. QR Validation
15. Emergency Management
16. Notifications
17. Database Architecture
18. API Design Standards
19. Security Requirements
20. Logging & Monitoring
21. Offline Strategy
22. Performance Requirements
23. Scalability
24. Deployment Architecture
25. Testing Strategy
26. Future Enhancements

---

# 1. Introduction

## Purpose

This document describes the complete technical design and implementation requirements for ConstructPulse.

It serves as the primary technical reference for developers, architects, QA engineers, DevOps engineers, and future contributors responsible for building and maintaining the platform.

Unlike the Product Requirements Document (PRD), which defines **what** the system should accomplish, this Technical Requirements Document specifies **how** those requirements will be implemented.

---

## Scope

This document covers:

- System architecture
- Technical stack
- Database design
- Backend architecture
- Mobile architecture
- Authentication
- Authorization
- Attendance engine
- GPS validation
- QR validation
- Worker lifecycle
- Emergency systems
- Performance
- Security
- Scalability
- Deployment

---

## Objectives

The primary objectives of ConstructPulse are:

- Build a scalable enterprise workforce management platform.
- Support multiple construction companies.
- Support thousands of workers across hundreds of sites.
- Ensure accurate attendance using GPS + QR validation.
- Improve workforce visibility.
- Digitize health and safety workflows.
- Enable real-time emergency mustering.
- Maintain complete auditability for workforce activities.

---

## Design Principles

The system shall be designed around the following engineering principles.

### Modular Architecture

Each business module must remain independent and loosely coupled.

Examples include:

- Authentication
- Attendance
- Companies
- Sites
- Workforce
- Safety
- Emergency
- Reporting

Each module should expose clearly defined interfaces.

---

### Scalability

The architecture shall support horizontal growth without requiring significant redesign.

Target scalability:

- 100+ active construction sites
- 10,000+ registered workers
- Millions of attendance records
- Multiple client organizations

---

### Security First

Every endpoint shall require explicit authorization.

Every privileged action shall be audited.

Sensitive information shall never be stored unencrypted.

Authentication tokens shall expire automatically.

---

### Mobile First

The mobile application is the primary user interface.

The backend must therefore optimize:

- low latency
- small payloads
- efficient pagination
- battery-efficient location updates

---

### Production Readiness

The platform shall prioritize:

- maintainability
- observability
- fault tolerance
- reliability
- clean architecture
- extensibility

No implementation decisions should rely on demo-specific shortcuts.

---

## Intended Audience

This document is intended for:

- Software Architects
- Backend Developers
- Flutter Developers
- QA Engineers
- DevOps Engineers
- Product Managers
- Technical Stakeholders
- Limelite Construction IT Team

---

## Definitions

| Term | Definition |
|------|------------|
| Company | Client organization using ConstructPulse |
| Site | Physical construction project location |
| Worker | Registered employee or subcontractor worker |
| Site Manager | User responsible for managing one or more sites |
| Operations Manager | Company-wide operational administrator |
| Attendance Session | Active check-in/check-out record |
| Geofence | GPS boundary defining a valid attendance area |
| QR Session | Site-specific QR validation process |
| Emergency Muster | Live worker accountability process during emergencies |

---

## Technical Philosophy

ConstructPulse follows a service-oriented modular architecture.

Each subsystem has a single responsibility and communicates through well-defined APIs.

Business logic remains centralized within the backend while the Flutter application functions primarily as a presentation layer and workflow orchestrator.

This approach ensures:

- consistent business rules
- simplified maintenance
- easier testing
- future web compatibility
- API-first development

---

## References

This document should be read alongside:

- PRD.md
- Database Overview
- API Specification
- Deployment Guide
- Architecture Document

# 2. Technical Goals

## Overview

The technical goals of ConstructPulse define the engineering standards that the platform must satisfy throughout its lifecycle.

These goals establish the baseline expectations for scalability, maintainability, security, reliability, and operational performance. Every architectural and implementation decision should align with these objectives.

The platform is intended to operate as an enterprise-grade workforce management solution for construction companies and therefore must prioritize long-term sustainability over short-term implementation convenience.

---

## 2.1 Scalability

The platform shall support organizational growth without requiring architectural redesign.

The system must scale horizontally as additional companies, projects, sites, and workers are onboarded.

### Initial Production Capacity

- 1 Client Organization (Limelite Construction)
- 100+ Active Construction Sites
- 10,000+ Registered Workers
- 200+ Site Managers
- Unlimited Attendance Records
- Unlimited Historical Reports

### Future Capacity

The architecture shall support multi-tenant expansion where multiple independent construction companies can operate securely within the same platform.

Each tenant shall have complete logical isolation of:

- Users
- Sites
- Attendance
- Departments
- Reports
- Configuration
- Documents

---

## 2.2 Availability

The platform shall remain operational during normal business hours with minimal downtime.

### Target Availability

99.9%

### Planned Maintenance

System maintenance shall be performed outside standard working hours whenever possible.

Critical attendance functionality should remain available during minor backend maintenance whenever practical.

---

## 2.3 Reliability

Attendance data represents operational and payroll information and therefore must never be silently lost.

The platform shall guarantee:

- Atomic attendance transactions
- Database consistency
- Safe rollback on failures
- Duplicate attendance prevention
- Accurate worker occupancy

Unexpected failures shall never result in partially completed attendance records.

---

## 2.4 Performance

The application must provide a responsive user experience across modern Android devices.

### Performance Targets

Dashboard Loading

- Less than 2 seconds

QR Validation

- Less than 2 seconds

Attendance Submission

- Less than 3 seconds

Worker Search

- Less than 1 second

Site Dashboard Refresh

- Less than 2 seconds

Emergency Muster Generation

- Less than 5 seconds

API Average Response Time

- Less than 500 milliseconds (excluding network latency)

---

## 2.5 Security

Security shall be considered a core architectural requirement rather than an optional feature.

The platform shall implement:

- JWT Authentication
- Refresh Tokens
- Role-Based Access Control (RBAC)
- HTTPS Communication
- Encrypted Local Storage
- Audit Logging
- Permission Validation
- Secure Passwordless Authentication (OTP)

Sensitive information shall never be exposed through client-side logic.

All authorization decisions shall be validated by the backend.

---

## 2.6 Maintainability

The codebase shall follow Clean Architecture principles.

Business logic, presentation, networking, and persistence layers shall remain independent wherever possible.

Every major module shall have a clearly defined responsibility.

Examples include:

- Authentication
- Attendance
- Workforce
- Sites
- Companies
- Safety
- Emergency
- Reporting

Future developers should be able to extend existing modules without introducing breaking changes into unrelated parts of the system.

---

## 2.7 Extensibility

ConstructPulse shall be designed to accommodate future business requirements with minimal refactoring.

Future modules expected include:

- Payroll Integration
- Visitor Management
- Equipment Tracking
- Vehicle Tracking
- Incident Reporting
- Document Management
- AI Workforce Analytics
- IoT Device Integration
- Digital Permit Management

The existing architecture shall not require major redesign to support these additions.

---

## 2.8 Usability

The mobile application is the primary interface used by construction workers in outdoor environments.

The interface shall therefore prioritize:

- Large touch targets
- High contrast visuals
- Minimal navigation depth
- Fast workflows
- Offline tolerance
- Clear feedback messages
- Minimal typing

Common workflows such as attendance should require no more than a few user interactions.

---

## 2.9 Compliance

The platform shall support operational compliance with New Zealand construction industry practices.

This includes maintaining digital records for:

- Worker registration
- Attendance history
- Site induction
- Safety acknowledgements
- Emergency musters
- Audit trails

The system shall preserve historical records for reporting and compliance purposes.

---

## 2.10 Observability

Production deployments shall provide sufficient operational visibility for troubleshooting and monitoring.

The platform should generate structured logs for:

- Authentication events
- Worker approvals
- Attendance transactions
- Site assignments
- Emergency events
- Administrative actions
- System errors

Logs should include timestamps, user identifiers, site identifiers, and request correlation IDs where applicable.

---

## 2.11 Fault Tolerance

The platform shall degrade gracefully during failures.

Examples include:

- Temporary network interruptions
- GPS signal loss
- API timeouts
- Database retry scenarios

User-facing error messages shall remain clear and actionable.

Unexpected exceptions shall never expose internal implementation details to end users.

---

## 2.12 Data Integrity

ConstructPulse shall enforce strict business rules to maintain data consistency.

Examples include:

- One active attendance session per worker
- One active check-in per site
- No duplicate worker registrations
- Attendance only within authorized geofences
- Worker approval required before attendance
- Complete audit trail for administrative actions

Critical transactions shall be executed atomically to prevent inconsistent records.

---

## 2.13 Future Readiness

The architecture shall support future evolution without significant redesign.

Potential future enhancements include:

- Progressive Web Application (PWA)
- Native iOS deployment
- Desktop administration portal
- Third-party payroll integration
- Government compliance reporting
- AI-assisted workforce planning
- Wearable device integration
- BIM and IoT integrations

Current architectural decisions should not restrict these future capabilities.

---

## Technical Success Criteria

The technical architecture shall be considered successful when it satisfies the following objectives:

- Supports enterprise-scale workforce operations.
- Provides reliable real-time attendance tracking.
- Maintains secure separation of organizational data.
- Delivers responsive performance under expected production loads.
- Enables modular expansion without architectural rewrites.
- Provides comprehensive auditability for all critical business operations.
- Supports long-term maintainability through clean architectural principles.

# 3. System Architecture

## Overview

ConstructPulse follows a layered, service-oriented architecture designed for enterprise-scale construction workforce management.

The platform separates presentation, business logic, persistence, and infrastructure concerns into independent layers to improve maintainability, scalability, and security.

The architecture follows an API-first approach, allowing future expansion to additional client applications such as web portals, desktop dashboards, and third-party integrations without requiring backend redesign.

---

# 3.1 Architectural Principles

The platform is designed around the following architectural principles:

- Separation of Concerns
- Single Responsibility Principle
- API-First Development
- Modular Design
- Role-Based Security
- Stateless Backend Services
- Scalable Infrastructure
- Database Consistency
- Fault Isolation
- Production Readiness

Each layer is responsible for one clearly defined purpose and communicates only through well-defined interfaces.

---

# 3.2 High-Level Architecture

```

```
                    +--------------------------------+
                    |      Mobile Application        |
                    |           Flutter              |
                    +---------------+----------------+
                                    |
                                    |
                           HTTPS / REST API
                                    |
                                    ▼
                    +--------------------------------+
                    |          FastAPI API           |
                    | Authentication & Routing       |
                    +---------------+----------------+
                                    |
                    Business Services Layer
                                    |
            +-----------+------------+-------------+
            |           |            |             |
            ▼           ▼            ▼             ▼
     Attendance    Workforce     Sites      Companies
      Service       Service      Service      Service
            |           |            |             |
            +-----------+------------+-------------+
                            |
                            ▼
                  SQLAlchemy ORM Layer
                            |
                            ▼
                    PostgreSQL Database

```

```

The backend remains completely independent of the mobile application.

Any future frontend can consume the same REST API.

---

# 3.3 Client Architecture

The Flutter application follows Clean Architecture.

```

```
Presentation Layer

↓

State Management (Riverpod)

↓

Repositories

↓

Network Layer (Dio)

↓

REST API

```

```

### Responsibilities

Presentation Layer

- User Interface
- Navigation
- Form Validation
- State Rendering

State Management

- Authentication State
- Attendance State
- Worker State
- Site State

Repositories

- Business abstraction
- API communication
- Local caching

Network Layer

- HTTP communication
- Token handling
- Request interception
- Error handling

---

# 3.4 Backend Architecture

The backend follows a modular service architecture.

```

```
FastAPI

↓

API Endpoints

↓

Business Services

↓

Repositories

↓

SQLAlchemy ORM

↓

PostgreSQL

```

```

Each module owns its own business logic.

Examples include:

- Authentication
- Attendance
- Workforce
- Sites
- Companies
- Safety
- Emergency

Business rules shall never reside in API controllers.

Controllers are responsible only for:

- Request validation
- Authorization
- Response generation

---

# 3.5 Module Architecture

The platform is divided into independent functional modules.

## Authentication Module

Responsibilities

- OTP Login
- JWT Generation
- Refresh Tokens
- Session Management

---

## Company Module

Responsibilities

- Company Management
- Departments
- Subcontractors
- Company Settings

---

## Site Module

Responsibilities

- Site Creation
- GPS Configuration
- QR Management
- Site Contacts
- Site Documents

---

## Workforce Module

Responsibilities

- Worker Registration
- Worker Approval
- Role Assignment
- Worker Transfers
- Certifications

---

## Attendance Module

Responsibilities

- QR Attendance
- GPS Validation
- Attendance History
- Live Occupancy
- Site Transfers

---

## Safety Module

Responsibilities

- Safety Induction
- PPE Checklist
- Site Instructions
- Toolbox Talks

---

## Emergency Module

Responsibilities

- Emergency Muster
- Occupancy Snapshot
- Missing Worker Detection
- Emergency Contacts

---

## Reporting Module

Responsibilities

- Attendance Reports
- Workforce Reports
- Compliance Reports
- Operational Analytics

---

# 3.6 Request Lifecycle

Every request follows a standardized processing pipeline.

```

```
User Action

↓

Flutter UI

↓

Riverpod Provider

↓

Repository

↓

Dio HTTP Client

↓

FastAPI Endpoint

↓

Authorization

↓

Business Service

↓

Database

↓

Response

↓

Flutter UI Update

```

```

Business logic shall only execute after successful authentication and authorization.

---

# 3.7 Data Flow

Example:

Worker Attendance

```

```
Worker

↓

QR Scan

↓

GPS Location

↓

Attendance API

↓

Authentication

↓

Permission Validation

↓

Site Validation

↓

GPS Validation

↓

Attendance Rules

↓

Database Transaction

↓

Attendance Created

↓

Dashboard Updated

```

```

Every attendance transaction must be fully validated before database persistence.

---

# 3.8 Multi-Tenant Architecture

ConstructPulse is designed as a multi-tenant platform.

Each company represents an isolated tenant.

```

```
ConstructPulse Platform

│

├── Limelite Construction

│ ├── Sites

│ ├── Workers

│ ├── Attendance

│ └── Reports

│

├── Company B

│ ├── Sites

│ ├── Workers

│ └── Attendance

│

└── Company C

```

```

Every authenticated request shall be scoped to the user's company.

Cross-company data access is strictly prohibited.

Only the Platform Owner may access multiple tenants.

---

# 3.9 Role Hierarchy

The platform enforces hierarchical authority.

```

```
Platform Owner

↓

Company Administrator

↓

Operations Manager

↓

Site Manager

↓

Supervisor

↓

Worker

```

```

Higher-level roles inherit the operational visibility of lower levels where explicitly permitted.

No user may elevate their own privileges.

Role assignment is performed only by authorized personnel.

---

# 3.10 Integration Architecture

The platform integrates with external services.

Current integrations include:

### Firebase Authentication

Purpose

- OTP Verification
- Identity Validation

---

### Google Maps Platform

Purpose

- GPS Coordinates
- Geolocation
- Distance Validation

---

### QR Code Generator

Purpose

- Site QR Generation
- Attendance Verification

---

Future integrations may include:

- Xero
- MYOB
- Microsoft Entra ID
- Power BI
- Government Compliance APIs
- IoT Sensors
- Wearable Devices

---

# 3.11 Design Decisions

The following architectural decisions have been intentionally adopted.

### REST APIs

Chosen because:

- Platform independent
- Mobile friendly
- Easy integration
- Mature ecosystem

---

### PostgreSQL

Chosen because:

- ACID compliance
- Strong relational support
- Excellent scalability
- Mature indexing

---

### FastAPI

Chosen because:

- High performance
- Automatic OpenAPI generation
- Type safety
- Asynchronous support

---

### Flutter

Chosen because:

- Cross-platform development
- High performance
- Single codebase
- Native-like experience

---

### Riverpod

Chosen because:

- Predictable state management
- Compile-time safety
- Testability
- Scalability

---

# 3.12 Architectural Constraints

The following constraints apply to the platform.

- All business logic must execute on the backend.
- Mobile applications shall never enforce security rules independently.
- Database access shall only occur through ORM repositories.
- Direct database access from the client is prohibited.
- Authentication is mandatory for all protected APIs.
- Every privileged operation must generate an audit log.
- Every attendance transaction must execute within a database transaction.

---

# 3.13 Architecture Summary

The ConstructPulse architecture is designed to provide:

- Enterprise scalability
- Modular development
- Clean separation of responsibilities
- High maintainability
- Secure multi-tenant operation
- Production-grade reliability
- Future extensibility

This architecture establishes the technical foundation for all subsequent implementation described throughout this document.

# 4. Technology Stack

## Overview

ConstructPulse is built using a modern, scalable technology stack designed for enterprise workforce management systems.

The selected technologies prioritize:

- Scalability
- Security
- Maintainability
- Performance
- Cross-platform compatibility
- Long-term support
- Rapid development

The stack has been selected to support future expansion into multiple organizations, thousands of workers, and geographically distributed construction sites.

---

# 4.1 Frontend Technology Stack

## Mobile Application

Technology

Flutter

Version

Flutter Stable (Latest LTS)

Purpose

Cross-platform mobile application.

Reason for Selection

- Single codebase for Android and iOS
- Excellent UI performance
- Rich widget ecosystem
- Native-like experience
- Strong community support
- Google-backed framework

Future Scope

Native desktop and web applications can also reuse significant portions of the Flutter codebase.

---

## Programming Language

Technology

Dart

Purpose

Frontend application development.

Reason for Selection

- Optimized for Flutter
- Strong typing
- Excellent asynchronous programming
- High runtime performance
- Null safety support

---

## State Management

Technology

Riverpod

Purpose

Application state management.

Responsibilities

- Authentication State
- Worker State
- Attendance State
- Site State
- Dashboard State

Reason for Selection

- Compile-time safety
- Dependency injection
- Testability
- Modular architecture
- Reduced boilerplate

---

## Navigation

Technology

GoRouter

Purpose

Application routing.

Responsibilities

- Role-based routing
- Authentication guards
- Deep linking
- Nested navigation

Reason for Selection

- Official Flutter routing solution
- Simple route protection
- Declarative navigation

---

## Networking

Technology

Dio

Purpose

REST API communication.

Responsibilities

- HTTP Requests
- Authentication headers
- Token refresh
- Logging
- Retry handling
- Error handling

Reason for Selection

- Powerful interceptor support
- Better error management
- Multipart upload support
- Production-ready networking

---

## Secure Storage

Technology

Flutter Secure Storage

Purpose

Secure storage of:

- JWT Access Tokens
- Refresh Tokens
- Session Information

Reason for Selection

Uses:

- Android Keystore
- Apple Keychain

Sensitive credentials are never stored in plain text.

---

# 4.2 Backend Technology Stack

## Framework

Technology

FastAPI

Language

Python

Purpose

REST API backend.

Responsibilities

- Authentication
- Business Logic
- Authorization
- API Validation
- Documentation

Reason for Selection

- High performance
- Automatic OpenAPI generation
- Async support
- Strong typing
- Excellent developer experience

---

## ORM

Technology

SQLAlchemy

Purpose

Database abstraction.

Responsibilities

- Entity Mapping
- Relationships
- Transactions
- Query Generation

Reason for Selection

- Mature ecosystem
- Production stability
- Flexible query capabilities
- Migration compatibility

---

## Database Migration

Technology

Alembic

Purpose

Schema version control.

Responsibilities

- Database migrations
- Schema upgrades
- Rollbacks

Benefits

- Version-controlled database
- Safe production deployment
- Team collaboration

---

## Authentication

Technology

Firebase Authentication

Method

Phone OTP

Responsibilities

- OTP Verification
- Identity Validation
- Session Establishment

Reason for Selection

- Reliable OTP delivery
- Google infrastructure
- High availability
- Fraud protection

---

## JWT Authentication

Technology

JSON Web Tokens

Purpose

API authentication.

Token Types

- Access Token
- Refresh Token

Benefits

- Stateless authentication
- High performance
- Mobile friendly
- Secure authorization

---

# 4.3 Database

Technology

PostgreSQL

Purpose

Primary relational database.

Reason for Selection

- ACID compliant
- High reliability
- Excellent indexing
- Complex relationship support
- Enterprise adoption

Core Features Used

- Foreign Keys
- Transactions
- Indexes
- Constraints
- UUID Primary Keys
- Enum Types

---

# 4.4 Maps & Location Services

Technology

Google Maps Platform

Purpose

Location validation.

Responsibilities

- GPS Coordinates
- Distance Calculation
- Reverse Geocoding
- Site Radius Validation

Production Usage

Attendance will only be accepted when the worker is physically present within the configured site boundary.

---

# 4.5 QR Technology

Technology

QR Code Generation

Purpose

Attendance identification.

Each construction site receives a unique QR code.

The QR code represents the construction site identity and cannot independently validate attendance.

Attendance is only completed after:

- QR validation
- GPS validation
- Worker authorization
- Active employment verification

---

# 4.6 Development Tools

## IDE

Visual Studio Code

Primary development environment.

---

## Version Control

Git

Purpose

Source code management.

Repository Strategy

- Main Branch
- Feature Branches
- Pull Requests

---

## API Testing

Swagger UI

Automatically generated through FastAPI.

Purpose

- Endpoint verification
- Request testing
- Response validation

---

## Database Administration

pgAdmin / PostgreSQL CLI

Purpose

Database inspection and management.

---

# 4.7 Development Standards

The project follows the following engineering standards.

Frontend

- Clean Architecture
- Feature-first folder structure
- Riverpod providers
- Repository pattern
- Immutable state

Backend

- Layered architecture
- Dependency injection
- Service layer
- Repository abstraction
- RESTful APIs

General

- SOLID Principles
- DRY Principle
- KISS Principle
- Type Safety
- Separation of Concerns

---

# 4.8 Repository Structure

The project is organized into two primary applications.

```
ConstructPulse/

├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
│
├── mobile/
│   ├── lib/
│   ├── assets/
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
│
├── docs/
│
├── README.md
│
└── .gitignore
```

This separation enables both applications to evolve independently while communicating through stable REST APIs.

---

# 4.9 Environment Configuration

The application uses environment variables for sensitive configuration.

Examples include:

Backend

- Database URL
- JWT Secret
- Firebase Credentials
- API Keys

Frontend

- API Base URL
- Google Maps Key
- Feature Flags

Sensitive information is never committed to source control.

---

# 4.10 Scalability Considerations

The selected technology stack supports future scaling through:

- Horizontal backend scaling
- Load balancing
- Database replication
- CDN integration
- Object storage
- Background workers
- Push notification services
- Multiple company tenants
- Thousands of concurrent workers

---

# 4.11 Future Technology Integrations

The architecture supports future integration with:

- Microsoft Entra ID
- Xero Payroll
- MYOB
- Power BI
- Microsoft Power Automate
- Government compliance systems
- IoT safety sensors
- RFID access systems
- Wearable safety devices
- AI-powered analytics
- Predictive workforce planning

---

# 4.12 Technology Stack Summary

The selected technology stack provides:

- Enterprise-grade security
- High availability
- Excellent developer productivity
- Cross-platform compatibility
- Long-term maintainability
- Strong community support
- Production scalability
- Cloud deployment readiness

This stack establishes a reliable technical foundation capable of supporting both the current workforce management requirements and future enterprise expansion.

# 5. User Roles & Permission Matrix

## Overview

ConstructPulse implements a hierarchical Role-Based Access Control (RBAC) model to ensure users only access the information and functionality required for their responsibilities.

Every authenticated user is assigned exactly one primary role.

Permissions are granted based on role assignments and, where applicable, scoped to specific companies and construction sites.

The permission model follows the Principle of Least Privilege, ensuring that users cannot access data beyond their operational responsibilities.

---

# 5.1 Role Hierarchy

The platform follows the organizational hierarchy below.

```

```
Platform Owner
        │
        ▼
Company Administrator
        │
        ▼
Operations Manager
        │
        ▼
Site Manager
        │
        ▼
Supervisor
        │
        ▼
Worker
```

```

Each level inherits operational visibility where explicitly permitted but cannot exceed permissions granted by the Company Administrator.

---

# 5.2 Platform Owner

## Description

The Platform Owner manages the ConstructPulse platform itself.

This role is intended only for ConstructPulse administrators or implementation engineers.

Platform Owners are not employees of Limelite Construction.

---

## Responsibilities

- Manage companies
- Create companies
- Configure subscription plans
- Enable platform-wide settings
- View platform analytics
- Support customer organizations
- Perform maintenance
- Manage system configurations

---

## Permissions

✓ Create companies

✓ Disable companies

✓ View all companies

✓ View all users

✓ View all sites

✓ Reset company administrators

✓ Configure platform settings

✓ Access system logs

✓ View audit logs

✗ Cannot mark attendance

✗ Cannot participate as site personnel

---

# 5.3 Company Administrator

## Description

The Company Administrator is responsible for managing an individual construction company.

Typically this role belongs to:

- Director
- Operations Administrator
- Office Administrator
- HR Manager

The Company Administrator has complete control over company data.

---

## Responsibilities

- Manage company settings
- Create construction sites
- Register managers
- Register supervisors
- Register workers
- Manage subcontractor companies
- Approve worker registrations
- Manage workforce
- Configure emergency contacts
- Configure safety content

---

## Permissions

✓ Create sites

✓ Archive sites

✓ Assign Site Managers

✓ Assign Operations Managers

✓ Assign Supervisors

✓ Approve workers

✓ Reject workers

✓ Suspend workers

✓ Transfer workers

✓ View all reports

✓ Configure departments

✓ Configure subcontractor companies

✓ Manage company documents

---

# 5.4 Operations Manager

## Description

Operations Managers oversee multiple construction sites simultaneously.

They coordinate workforce allocation across projects.

---

## Responsibilities

- Monitor site operations
- Allocate workforce
- Monitor attendance
- Review compliance
- Coordinate site managers

---

## Permissions

✓ View all assigned sites

✓ Transfer workers

✓ View attendance

✓ View analytics

✓ View emergency reports

✓ Generate reports

✗ Cannot modify company settings

✗ Cannot create Company Admins

---

# 5.5 Site Manager

## Description

Each construction site has one or more Site Managers.

Site Managers are responsible only for their assigned sites.

---

## Responsibilities

- Approve workers arriving at site
- Manage daily attendance
- Monitor workforce
- Conduct inductions
- Handle emergencies

---

## Permissions

✓ View assigned site

✓ View assigned workers

✓ Approve pending workers

✓ Reject pending workers

✓ Suspend workers

✓ Reactivate workers

✓ Transfer workers into assigned sites

✓ Remove workers from assigned sites

✓ Generate site reports

✓ Update emergency contacts

✓ Upload site notices

✓ Manage site QR codes

✗ Cannot access other sites

✗ Cannot modify company settings

---

# 5.6 Supervisor

## Description

Supervisors manage crews during daily operations.

A supervisor reports to the Site Manager.

---

## Responsibilities

- Supervise crews
- Verify attendance
- Report incidents
- Monitor compliance

---

## Permissions

✓ View assigned workers

✓ View attendance

✓ View emergency status

✓ View safety acknowledgements

✓ Submit incident reports

✗ Cannot approve registrations

✗ Cannot create users

✗ Cannot modify sites

---

# 5.7 Worker

## Description

Workers perform operational construction activities.

Workers may belong to Limelite directly or a subcontractor company.

Workers may be assigned to multiple sites.

---

## Responsibilities

- Complete registration
- Complete safety induction
- Scan QR codes
- Mark attendance
- Update profile
- View assigned sites
- View attendance history

---

## Permissions

✓ QR Check-In

✓ QR Check-Out

✓ View profile

✓ View assigned sites

✓ View attendance

✓ Complete induction

✓ Call emergency contacts

✓ Access safety documentation

✗ Cannot modify workforce

✗ Cannot approve users

✗ Cannot view other workers

---

# 5.8 Subcontractor Company

## Description

A subcontractor company supplies workers to Limelite Construction.

Examples include:

- Electrical Contractors
- Plumbing Contractors
- Scaffolding Contractors
- Steel Fixing Contractors
- Concrete Contractors

The subcontractor itself is registered within the platform.

Its workers become part of Limelite's operational workforce while remaining associated with their employer.

---

## Responsibilities

- Maintain company details
- Supply workforce
- Maintain certifications

---

## Permissions

Company records include:

- Company Name

- Contact Person

- Phone Number

- Email

- Trade Category

- Company Address

- Insurance Information

- Compliance Status

Workers linked to subcontractors display both:

Employer:
ABC Electrical Ltd

Working For:
Limelite Construction

---

# 5.9 Permission Matrix

| Capability | Platform Owner | Company Admin | Operations Manager | Site Manager | Supervisor | Worker |
|------------|----------------|---------------|--------------------|--------------|------------|--------|
| View Company | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create Site | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Assign Site Manager | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Approve Worker | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Reject Worker | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Suspend Worker | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Transfer Worker | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| View Reports | ✓ | ✓ | ✓ | Site Only | Site Only | Own Only |
| Emergency Muster | ✓ | ✓ | ✓ | ✓ | ✓ | Participate |
| Manage QR Codes | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Configure Safety | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Check In/Out | ✗ | Optional | Optional | Optional | Optional | ✓ |

---

# 5.10 Role Assignment Workflow

Role assignment is centrally controlled.

1. Platform Owner creates a company.
2. Platform Owner assigns the first Company Administrator.
3. Company Administrator creates Operations Managers.
4. Company Administrator creates Site Managers.
5. Site Managers invite or approve workers for their assigned sites.
6. Workers complete registration using OTP.
7. Site Managers review registrations and approve or reject access.
8. Approved workers receive access to assigned sites.
9. Attendance is enabled only after approval and successful safety induction.

No user may assign a role equal to or higher than their own.

---

# 5.11 Security Principles

The RBAC implementation follows the following principles:

- Least Privilege Access
- Company Isolation
- Site-Level Access Control
- Audit Logging
- Immutable Permission Validation
- Backend-Enforced Authorization

All permissions are validated by the backend.

Frontend permissions are used only to control the user interface and are never considered a security boundary.

---

# 5.12 Role Summary

The ConstructPulse permission model provides:

- Clear organizational hierarchy
- Secure multi-tenant isolation
- Site-level operational control
- Scalable workforce management
- Fine-grained access permissions
- Enterprise-grade authorization

This RBAC model supports organizations ranging from small contractors to nationwide construction companies while maintaining security, flexibility, and operational efficiency.

# 5.13 Approval Workflow Engine

ConstructPulse supports configurable workforce approval workflows.

Different construction companies operate with different organizational structures. Therefore, approval responsibility is configurable at the company level rather than hardcoded into the application.

A company may select one of the following workflows.

## Workflow A — Company Administrator Approval

Worker Registers

↓

Company Administrator Reviews

↓

Approved / Rejected

---

## Workflow B — Site Manager Approval

Worker Registers

↓

Assigned Site Manager Reviews

↓

Approved / Rejected

---

## Workflow C — Supervisor Recommendation

Worker Registers

↓

Supervisor Reviews

↓

Site Manager Final Approval

↓

Approved / Rejected

---

## Workflow D — Hybrid Approval

Internal Employees

↓

Auto Approved

Subcontractors

↓

Manual Review

↓

Approved / Rejected

---

The approval workflow is configurable through Company Settings and may be changed without requiring application code changes.

# 6. Business Workflows

## Overview

ConstructPulse is designed around the day-to-day operational workflows of construction companies rather than individual software features.

Each workflow models a real-world business process performed by construction personnel, ensuring that the platform supports operational efficiency, workforce accountability, safety compliance, and regulatory requirements.

Business workflows are enforced by backend business rules and role-based permissions. Every workflow generates audit records to ensure traceability and accountability.

The following workflows define the operational lifecycle of a worker, site, and project within the platform.

---

# 6.1 Workflow Index

The platform currently supports the following business workflows:

1. Company Onboarding
2. Site Creation & Configuration
3. Workforce Registration
4. Configurable Worker Approval
5. Safety Induction
6. Site Assignment
7. QR Attendance & GPS Validation
8. Site Transfer
9. Daily Attendance Management
10. Emergency Muster
11. Incident Reporting
12. Worker Lifecycle Management
13. Subcontractor Management
14. Operational Reporting
15. Administrative Management

Each workflow is described in detail in the following sections.

# 6.2 Company Onboarding Workflow

## Overview

The Company Onboarding Workflow establishes a new organization within the ConstructPulse platform.

This workflow is executed once for every customer organization and is typically performed by the Platform Owner or an authorized implementation engineer during initial deployment.

The objective is to create a secure, isolated tenant containing all organizational information, administrative users, construction sites, and operational settings required before daily workforce activities can begin.

---

## Actors

Primary Actor

- Platform Owner

Secondary Actors

- Company Administrator

---

## Preconditions

Before onboarding begins:

- Customer agreement completed
- Company information available
- Primary administrator identified
- Initial construction sites identified (optional)

---

## Workflow

Step 1

Platform Owner creates a new company.

Required information includes:

- Company Name
- Legal Business Name
- NZBN (optional)
- Company Address
- Contact Email
- Primary Contact Number
- Company Logo
- Time Zone
- Country
- Default Language

---

Step 2

The Platform automatically provisions an isolated tenant.

The following resources are created:

- Company Record
- Company Settings
- Audit Log
- Default Departments
- Default Permission Configuration

---

Step 3

The Platform Owner creates the first Company Administrator.

Required information:

- Full Name
- Mobile Number
- Email Address
- Job Title

---

Step 4

An invitation is sent to the Company Administrator.

The administrator completes OTP verification and activates their account.

---

Step 5

The Company Administrator completes the initial company configuration.

Configuration includes:

- Approval Workflow
- Emergency Contacts
- Company Branding
- Safety Policies
- Working Hours
- GPS Attendance Radius
- Default Site Settings

---

Step 6

Construction sites are created.

Each site receives:

- Site Name
- Address
- GPS Coordinates
- QR Code
- Emergency Information
- Assigned Site Manager

---

Step 7

The company is marked as operational.

Worker registration is enabled.

Attendance functionality becomes available.

---

## Postconditions

After successful onboarding:

- Company exists as an isolated tenant.
- Company Administrator has full administrative access.
- Initial sites are operational.
- Workers may begin registering.
- Attendance workflows become available.

---

## Business Rules

- Company names must be unique within the platform.
- Every company must have at least one Company Administrator.
- Every company maintains isolated data.
- Only Platform Owners may create companies.
- Company deletion is prohibited if operational data exists.

---

## Failure Scenarios

- Duplicate company detected.
- Invalid administrator details.
- Company configuration incomplete.
- Required information missing.
- Platform provisioning failure.

---

## Audit Events

The following events are recorded:

- Company Created
- Company Activated
- Administrator Assigned
- Company Configuration Updated
- Initial Site Created

---

## Future Enhancements

Future versions may support:

- Self-service company onboarding
- Subscription plan selection
- Digital agreement signing
- Automated billing integration
- Azure Active Directory integration
- Microsoft Entra ID integration
- SSO configuration

# 6.3 Site Creation & Configuration Workflow

## Overview

The Site Creation & Configuration Workflow establishes a new construction site within the ConstructPulse platform.

Each construction site represents an operational workplace where workers perform daily activities, record attendance, complete safety inductions, and participate in emergency procedures.

A site must be fully configured before workers can be assigned or attendance can be recorded.

This workflow ensures every site follows a standardized operational and safety setup while allowing company-specific customization.

---

## Actors

Primary Actors

- Company Administrator
- Operations Manager (if permitted)

Secondary Actors

- Site Manager

---

## Preconditions

Before a site can be created:

- Company must exist.
- Company Administrator account must be active.
- Company onboarding must be completed.
- GPS services must be available.
- Required company settings must be configured.

---

## Workflow

### Step 1 — Create New Site

The Company Administrator initiates the creation of a new construction site.

Required information:

- Site Name
- Project Name
- Site Address
- Client Name (Optional)
- Project Number (Optional)
- Site Description

---

### Step 2 — Configure Site Location

The administrator selects the exact construction site location.

Configuration includes:

- GPS Latitude
- GPS Longitude
- Attendance Radius
- Site Boundary
- Muster Point Location

The GPS coordinates become the official reference location for attendance validation.

---

### Step 3 — Configure Site Information

Operational details are configured.

Examples include:

- Working Hours
- Shift Timings
- Weekend Schedule
- Public Holiday Rules
- Maximum Worker Capacity
- Expected Completion Date
- Site Status

---

### Step 4 — Generate Site QR Code

ConstructPulse generates a unique QR Code for the site.

The QR Code contains:

- Site Identifier
- Company Identifier
- QR Version
- Security Signature

The QR Code does not directly record attendance.

Instead, it identifies the site so that additional validation can occur.

---

### Step 5 — Configure Attendance Rules

Attendance settings are defined.

Examples include:

- GPS Required
- QR Mandatory
- Self Check-In Allowed
- Manual Attendance Allowed
- Late Arrival Threshold
- Early Checkout Rules
- Overtime Rules

Attendance is only accepted when all configured validation rules are satisfied.

---

### Step 6 — Configure Safety Information

Safety documentation is attached to the site.

Examples:

- Site Induction
- PPE Requirements
- Hazard Register
- Toolbox Talk Documents
- Emergency Procedures
- Site Maps
- Evacuation Routes

Workers must acknowledge mandatory safety information before attendance is enabled.

---

### Step 7 — Configure Emergency Contacts

Emergency information is entered.

Examples include:

Emergency Services

- NZ Emergency Number (111)

Site Contacts

- Site Manager
- Operations Manager
- Safety Officer
- First Aid Officer

Medical Facilities

- Nearest Hospital
- Nearest Medical Centre

Additional Contacts

- Poison Centre
- Fire Service
- Police

Emergency contacts remain accessible even when attendance is unavailable.

---

### Step 8 — Assign Site Management

The administrator assigns operational personnel.

Assignments include:

- Site Manager
- Supervisors
- Safety Officer
- First Aid Officer

Only assigned personnel receive management permissions for that site.

---

### Step 9 — Assign Approved Workers

Approved workers are assigned to the site.

Each assignment includes:

- Start Date
- Expected End Date
- Worker Role
- Employer
- Trade Category

Workers may belong to multiple active sites if authorized.

---

### Step 10 — Activate Site

After configuration is complete:

- Site becomes Active.
- QR Code becomes valid.
- GPS validation becomes active.
- Worker attendance is enabled.
- Site dashboards begin collecting operational data.

---

## Postconditions

After successful completion:

- Site is operational.
- QR attendance is available.
- Workers may be assigned.
- Emergency contacts are available.
- Safety documents are published.
- Site dashboards begin tracking live workforce activity.

---

## Business Rules

- Every site belongs to exactly one company.
- Every site must have at least one Site Manager.
- GPS coordinates are mandatory.
- Attendance radius must be configured.
- QR Codes must be unique.
- Site status determines attendance availability.
- Archived sites cannot accept attendance.
- Workers cannot check into inactive sites.

---

## Validation Rules

Before activation, ConstructPulse validates:

✓ Site Name

✓ Company Ownership

✓ GPS Coordinates

✓ Attendance Radius

✓ QR Generation

✓ Site Manager Assignment

✓ Emergency Contact Configuration

✓ Safety Documentation

Any validation failure prevents site activation.

---

## Failure Scenarios

Examples include:

- Duplicate Site Name
- Missing GPS Coordinates
- Invalid Attendance Radius
- QR Generation Failure
- No Site Manager Assigned
- Emergency Contact Missing
- Safety Configuration Incomplete

---

## Audit Events

The following events are recorded:

- Site Created
- Site Updated
- Site Activated
- Site Archived
- QR Regenerated
- GPS Updated
- Attendance Rules Modified
- Safety Documents Updated
- Emergency Contacts Updated
- Site Manager Assigned

---

## Production Considerations

The platform supports:

- Multiple active construction sites
- Simultaneous workforce allocation
- Dynamic attendance radius updates
- Temporary site closures
- Remote project locations
- Multi-stage construction projects
- Offline QR verification (future)
- GPS spoofing detection (future)

---

## Future Enhancements

Future releases may support:

- Interactive site maps
- Multiple muster points
- Temporary work zones
- IoT access gates
- NFC site access
- Bluetooth beacon verification
- Automated weather alerts
- Site-specific AI safety recommendations
- Integration with New Zealand Worksafe compliance systems

# 6.4 Workforce Registration Workflow

## Overview

The Workforce Registration Workflow allows new personnel to securely join the ConstructPulse platform.

The registration process is designed to collect all information required for workforce management, safety compliance, attendance tracking, emergency response, and site operations while ensuring that only verified individuals gain access to the platform.

Registration does not automatically grant access to construction sites.

Every registration enters a pending approval state until reviewed by the configured approval authority.

---

## Actors

Primary Actor

- Worker

Secondary Actors

- Company Administrator
- Operations Manager
- Site Manager
- Supervisor (Recommendation Workflow)

---

## Preconditions

Before registration can begin:

- The company must exist within ConstructPulse.
- The worker must possess a valid mobile number.
- OTP verification service must be available.
- The worker must not already have an active account.
- Required company registration settings must be configured.

---

# Registration Workflow

## Step 1 — Phone Number Verification

The worker enters their mobile number.

The platform performs the following validations:

- Valid phone number format
- Existing account lookup
- Duplicate registration check

If the phone number is not registered, the registration process begins.

If an account already exists, the worker is redirected to login.

---

## Step 2 — OTP Verification

A One-Time Password (OTP) is sent to the worker's mobile device.

The worker enters the received OTP.

The platform validates:

- OTP accuracy
- Expiration time
- Maximum retry attempts

Successful verification establishes the worker's identity.

---

## Step 3 — Personal Information

The worker completes their personal profile.

Required fields include:

- First Name
- Last Name
- Mobile Number
- Email Address (Optional)
- Profile Photo (Future)
- Preferred Language

---

## Step 4 — Employment Information

The worker provides employment details.

Required information:

- Employer

  - Limelite Construction
  - Approved Subcontractor Company

- Trade
- Job Title
- Department (Optional)
- Employee Number (If Applicable)

The employer determines future reporting relationships.

---

## Step 5 — Compliance Information

The worker provides mandatory compliance information.

Examples include:

- Working at Heights Certification
- First Aid Certification
- Electrical License
- Forklift License
- Confined Space Certification
- Crane Operator License
- Other Trade Certifications

Each certification records:

- Certificate Number
- Expiry Date
- Issuing Authority

Expired certifications are flagged for administrator review.

---

## Step 6 — Emergency Information

Emergency contact details are collected.

Required information:

- Emergency Contact Name
- Relationship
- Mobile Number

Optional information:

- Medical Conditions
- Allergies
- Blood Group
- Additional Notes

This information is only accessible to authorized personnel during emergencies.

---

## Step 7 — Preferred Site (Optional)

The worker may select one or more preferred construction sites.

This does not assign the worker.

It simply assists administrators during workforce allocation.

---

## Step 8 — Device Permissions

The application requests required permissions.

Mandatory:

- Location Permission
- Camera Permission

Optional:

- Notifications

Attendance functionality remains disabled until mandatory permissions are granted.

---

## Step 9 — Registration Submission

The worker reviews all submitted information.

ConstructPulse validates:

- Required fields
- Duplicate accounts
- Employer existence
- Trade validity
- Emergency contact completeness

Upon successful validation:

Worker Status

Pending Approval

---

## Step 10 — Pending Approval

The worker receives confirmation that registration has been submitted.

The application displays:

- Registration Status
- Approval Progress
- Company Contact Information
- Estimated Review Time

The worker cannot access operational features until approval is complete.

---

## Postconditions

After successful registration:

- Worker profile created
- Worker status set to Pending
- Approval workflow initiated
- Audit log generated
- Administrator notified

---

## Business Rules

- Mobile numbers must be unique.
- Duplicate registrations are prohibited.
- Workers cannot select administrative roles.
- Employer must exist before registration.
- Emergency contact information is mandatory.
- GPS permission is mandatory before attendance.
- Registration does not grant site access.

---

## Validation Rules

ConstructPulse validates:

✓ Phone Number

✓ OTP Verification

✓ Employer

✓ Trade

✓ Emergency Contact

✓ Required Fields

✓ Duplicate Worker

✓ Company Association

Registration fails if any mandatory validation is unsuccessful.

---

## Failure Scenarios

Examples include:

- Invalid OTP
- Duplicate Mobile Number
- Unknown Employer
- Missing Required Fields
- Expired Registration Session
- Network Failure
- Invalid Certification Information

---

## Audit Events

The following events are recorded:

- Registration Started
- OTP Verified
- Registration Submitted
- Worker Profile Created
- Registration Updated
- Registration Cancelled

---

## Security Considerations

The registration process incorporates multiple security measures.

- OTP-based identity verification
- Secure token generation
- Duplicate account prevention
- Backend validation
- Role assignment restrictions
- Audit logging

Sensitive worker information is encrypted and protected according to company privacy policies.

---

## Future Enhancements

Future versions may support:

- Passport or Driver License Verification
- Facial Verification
- Digital Signature Capture
- Automatic Certification Validation
- Government Identity Verification
- OCR Document Upload
- Biometric Authentication
- Offline Registration

# 6.5 Configurable Workforce Approval Workflow

## Overview

The Workforce Approval Workflow governs how newly registered personnel become authorized to work within the organization.

ConstructPulse does not hardcode a single approval process.

Instead, each company configures its preferred approval workflow during company onboarding.

This flexibility allows ConstructPulse to support organizations of different sizes, structures, and operational requirements without requiring software modifications.

Worker approval grants operational platform access but does not automatically authorize attendance at every construction site.

Additional compliance requirements may still apply.

---

# Objectives

The approval workflow is designed to:

- Verify worker identity
- Prevent unauthorized access
- Validate employment
- Ensure compliance requirements are satisfied
- Assign appropriate permissions
- Maintain complete audit history
- Support configurable organizational structures

---

# Actors

Primary Actors

- Company Administrator
- Operations Manager
- Site Manager

Secondary Actors

- Supervisor
- Worker

---

# Preconditions

Before approval begins:

- Worker registration completed.
- Worker status is Pending.
- Company approval workflow configured.
- Worker profile successfully created.
- Worker belongs to a valid employer.

---

# Supported Approval Models

ConstructPulse supports multiple approval models.

The selected workflow is configured at the company level.

---

## Model A — Company Administrator Approval

Registration

↓

Pending Queue

↓

Company Administrator Reviews

↓

Approve / Reject

↓

Worker Activated

---

Recommended for:

- Small companies
- Centralized administration

---

## Model B — Site Manager Approval

Registration

↓

Assigned Site Manager

↓

Approve / Reject

↓

Worker Activated

---

Recommended for:

- Medium-sized organizations
- Independent construction sites

---

## Model C — Supervisor Recommendation

Registration

↓

Supervisor Reviews

↓

Recommendation

↓

Site Manager Decision

↓

Worker Activated

---

Recommended for:

- Large projects
- Multi-level approval

---

## Model D — Hybrid Workflow

Internal Employees

↓

Automatic Approval

Subcontractors

↓

Manual Review

↓

Approval

---

Recommended for:

- Large construction companies
- Mixed workforce

---

# Approval Workflow

## Step 1 — Pending Queue

After registration, workers enter the Pending Workforce Queue.

Administrators see:

- Name
- Employer
- Trade
- Registration Date
- Preferred Site
- Certifications
- Registration Status

---

## Step 2 — Profile Review

Reviewer validates:

Personal Information

Employment

Employer

Trade

Emergency Contact

Required Certifications

Submitted Documents

Preferred Site

---

## Step 3 — Compliance Validation

ConstructPulse verifies:

Required Certifications

↓

Document Completeness

↓

Employer Status

↓

Company Policies

↓

Approval Eligibility

If compliance requirements are incomplete, approval cannot continue.

---

## Step 4 — Decision

Reviewer selects:

Approve

Reject

Request More Information (Future)

Suspend (Future)

Each decision requires:

Decision

Reason

Reviewer

Timestamp

---

## Step 5 — Automatic Actions

If Approved

ConstructPulse automatically:

- Activates account
- Enables login
- Assigns default permissions
- Creates audit record
- Sends notification

---

If Rejected

ConstructPulse automatically:

- Locks operational access
- Displays rejection screen
- Records rejection reason
- Sends notification

---

If Suspended

ConstructPulse automatically:

- Disables attendance
- Prevents login
- Records suspension
- Ends active attendance sessions

---

# Compliance Gate

Worker approval alone does not guarantee site access.

The worker must satisfy all compliance requirements.

```
Worker Registered

↓

Approved

↓

Required Certifications Valid

↓

Safety Induction Completed

↓

GPS Permission Granted

↓

Site Assigned

↓

Attendance Enabled
```

Only workers who successfully pass every stage become operational.

---

# Business Rules

- Every worker must pass through exactly one approval workflow.
- Workers cannot approve themselves.
- Approval permissions depend on company configuration.
- Every approval decision is audited.
- Approval does not bypass safety requirements.
- Rejected workers cannot access operational modules.
- Suspended workers cannot record attendance.

---

# Validation Rules

ConstructPulse validates:

✓ Worker Exists

✓ Pending Status

✓ Employer Exists

✓ Trade Exists

✓ Required Documents

✓ Required Certifications

✓ Reviewer Permission

✓ Company Scope

---

# Failure Scenarios

Examples include:

- Invalid reviewer
- Missing certification
- Duplicate approval request
- Worker already approved
- Company mismatch
- Expired registration
- Missing emergency information

---

# Audit Events

Every approval action generates immutable audit records.

Events include:

- Approval Requested
- Approval Reviewed
- Worker Approved
- Worker Rejected
- Worker Suspended
- Worker Reactivated
- Approval Workflow Changed

---

# Notifications

Notifications are generated for:

Worker

- Registration Received
- Approved
- Rejected
- Suspended

Administrator

- New Registration
- Approval Pending
- Compliance Missing

Site Manager

- New Worker Assigned
- Worker Approved

---

# Production Considerations

The approval engine is designed to support:

- Thousands of concurrent workers
- Multiple approval chains
- Multi-company deployments
- Site-specific approvals
- Temporary workers
- Seasonal workforce
- Labour hire companies
- International contractors

---

# Future Enhancements

Future releases may introduce:

- Multi-stage approvals
- Digital signatures
- AI-assisted document verification
- Automatic certification validation
- Approval SLA monitoring
- Escalation workflows
- Approval delegation during leave
- Integration with HR systems

# Approval Inbox

ConstructPulse provides every authorized reviewer with a centralized Approval Inbox.

The Approval Inbox presents all pending workforce actions requiring attention and prioritizes them based on urgency.

The inbox enables reviewers to efficiently process registrations while maintaining complete auditability.

---

## Inbox Sections

### 🔴 Requires Immediate Attention

Examples:

- Workers waiting longer than configured SLA
- Missing mandatory certifications
- Expired certifications
- Incomplete emergency contact information
- High-priority workforce requests

---

### 🟡 Pending Review

Examples:

- Newly registered workers
- Workers awaiting document verification
- Site transfer requests
- Contractor registrations

---

### 🟢 Recently Processed

Examples:

- Recently Approved Workers
- Recently Rejected Workers
- Recently Reactivated Workers
- Recently Suspended Workers

---

## Available Actions

Reviewers may:

- View Worker Profile
- View Certifications
- View Documents
- Approve
- Reject
- Request Additional Information (Future)
- Suspend (Future)
- Assign Site
- Assign Supervisor

---

## Search & Filtering

The inbox supports:

- Worker Name
- Employer
- Trade
- Registration Date
- Preferred Site
- Approval Status
- Assigned Reviewer
- Certification Status

---

## Service Level Agreement (Future)

Organizations may configure approval SLAs.

Example:

- Registration pending > 24 hours
- Registration pending > 48 hours
- Registration pending > 72 hours

Workers exceeding SLA are highlighted automatically.

---

## Audit Events

Every inbox action is recorded within the audit system.

Examples:

- Inbox Viewed
- Worker Opened
- Approval Completed
- Rejection Completed
- Assignment Completed

# 6.6 Safety Induction & Site Compliance Workflow

## Overview

The Safety Induction & Site Compliance Workflow ensures that every approved worker understands the safety requirements, operational procedures, and emergency protocols before entering a construction site.

Completion of the safety induction is mandatory before a worker can record attendance or perform work at any site.

Each construction site maintains its own induction requirements, allowing organizations to enforce site-specific compliance standards.

ConstructPulse maintains a complete audit trail of every completed induction for legal, operational, and health & safety compliance purposes.

---

# Objectives

The workflow is designed to:

- Ensure worker safety
- Meet New Zealand Health & Safety compliance requirements
- Reduce workplace incidents
- Verify worker understanding of site rules
- Record legally auditable induction acknowledgements
- Prevent unauthorized site access
- Standardize induction procedures across all projects

---

# Actors

Primary Actor

- Worker

Secondary Actors

- Site Manager
- Safety Officer
- Company Administrator
- Operations Manager

---

# Preconditions

Before induction begins:

- Worker registration completed.
- Worker approved.
- Worker assigned to at least one site.
- Site is active.
- Site induction has been configured.

---

# Induction Workflow

## Step 1 — Site Selection

The worker selects the assigned construction site.

ConstructPulse retrieves the site's induction package.

The induction package may differ between construction sites.

---

## Step 2 — Safety Briefing

The worker reviews mandatory safety information.

Examples include:

- Site Rules
- PPE Requirements
- Restricted Areas
- Hazard Register
- High-Risk Activities
- Working Hours
- Environmental Policies
- Visitor Rules

Workers cannot skip mandatory sections.

---

## Step 3 — Emergency Procedures

ConstructPulse displays:

- Emergency Evacuation Procedure
- Muster Point Location
- Emergency Exit Routes
- Fire Procedures
- Incident Reporting Process
- Medical Emergency Process

Emergency contact information includes:

- New Zealand Emergency Services (111)
- Site Manager
- Safety Officer
- First Aid Officer
- Nearest Hospital
- Company Emergency Contact

Workers acknowledge understanding before continuing.

---

## Step 4 — Site Map

Workers review the site layout.

The site map may identify:

- Entry Gates
- QR Check-in Locations
- Site Office
- Amenities
- Hazard Zones
- Restricted Areas
- First Aid Stations
- Fire Equipment
- Emergency Assembly Point

Future versions may include interactive maps.

---

## Step 5 — Safety Documents

Workers review required documentation.

Examples:

- Safe Work Method Statements (SWMS)
- Toolbox Talks
- Risk Assessments
- Environmental Controls
- Company Safety Policies
- Client Safety Requirements

Documents are version controlled.

---

## Step 6 — Knowledge Assessment

Companies may require a short induction assessment.

Examples:

- Multiple Choice Questions
- Hazard Identification
- Emergency Response Questions
- PPE Verification

Passing score requirements are configurable.

Workers failing the assessment may be required to repeat the induction.

---

## Step 7 — Worker Acknowledgement

The worker confirms:

✓ I have completed the induction.

✓ I understand the site rules.

✓ I agree to follow all safety requirements.

✓ I understand emergency procedures.

Future versions may support:

- Digital Signature
- Face Verification
- Supervisor Witness

---

## Step 8 — Compliance Verification

ConstructPulse verifies:

- Worker Approved
- Site Assignment
- Required Certifications
- Induction Completed
- Assessment Passed
- Required Documents Acknowledged

Only compliant workers proceed.

---

## Step 9 — Attendance Activation

After successful induction:

ConstructPulse automatically enables attendance for that site.

The worker may now:

- Scan QR Codes
- Record Attendance
- Participate in Emergency Muster

---

# Postconditions

After successful completion:

- Induction marked Complete.
- Compliance status updated.
- Attendance enabled.
- Audit records generated.
- Site Manager notified (Optional).

---

# Business Rules

- Every worker must complete induction before first attendance.
- Inductions are site-specific.
- Updated induction material requires re-acknowledgement.
- Expired inductions automatically disable attendance.
- Companies may require annual re-induction.
- Site Managers may invalidate inductions if required.

---

# Validation Rules

ConstructPulse validates:

✓ Worker Approved

✓ Site Assignment

✓ Required Certifications

✓ Required Documents

✓ Assessment Completion

✓ Worker Acknowledgement

✓ Site Status

Attendance remains disabled if any validation fails.

---

# Failure Scenarios

Examples include:

- Induction not completed.
- Assessment failed.
- Missing certifications.
- Site archived.
- Updated safety documents not acknowledged.
- Network interruption.
- Expired induction.

---

# Audit Events

Every action is recorded.

Examples include:

- Induction Started
- Document Viewed
- Assessment Completed
- Assessment Failed
- Induction Completed
- Induction Expired
- Re-Induction Required

---

# Notifications

Worker Notifications

- Induction Available
- Induction Completed
- Re-Induction Required
- Compliance Expired

Site Manager Notifications

- Worker Inducted
- Worker Non-Compliant
- Induction Expired

---

# Production Considerations

ConstructPulse supports:

- Site-specific inductions
- Company-wide inductions
- Multi-language induction content
- Offline document viewing (Future)
- Video-based inductions
- PDF acknowledgements
- Annual re-certification
- Client-specific induction packages

---

# Future Enhancements

Future releases may include:

- Video safety inductions
- AI-powered hazard recognition training
- Interactive site walkthroughs
- QR-based induction stations
- Digital signature capture
- Voice-guided inductions
- AR/VR safety simulations
- Integration with WorkSafe New Zealand compliance systems

# 6.7 Site Assignment & Workforce Allocation Workflow

## Overview

The Site Assignment & Workforce Allocation Workflow determines which construction sites a worker is authorized to access and work on.

Approval alone does not grant permission to enter every construction site.

Workers must be explicitly assigned to one or more active sites before attendance can be recorded.

This workflow enables organizations to efficiently allocate labour across multiple construction projects while maintaining complete operational visibility and security.

---

# Objectives

The workflow is designed to:

- Allocate workers to construction sites
- Control site-level access
- Support multi-site operations
- Prevent unauthorized attendance
- Enable workforce planning
- Maintain workforce allocation history
- Support temporary workforce movement

---

# Actors

Primary Actors

- Company Administrator
- Operations Manager

Secondary Actors

- Site Manager
- Supervisor

---

# Preconditions

Before assignment begins:

- Worker registration completed.
- Worker approved.
- Compliance Passport valid.
- Site exists.
- Site is active.

---

# Assignment Workflow

## Step 1 — Select Worker

The reviewer selects an approved worker.

ConstructPulse displays:

- Worker Profile
- Employer
- Trade
- Certifications
- Current Assignments
- Compliance Status

---

## Step 2 — Select Site

Reviewer selects one or more construction sites.

Displayed information includes:

- Site Name
- Project
- Capacity
- Current Workforce
- Site Status
- Site Manager

---

## Step 3 — Configure Assignment

Assignment details include:

- Assignment Type
- Start Date
- End Date (Optional)
- Shift
- Reporting Supervisor
- Assigned Site Manager
- Trade at Site

---

## Step 4 — Assignment Validation

ConstructPulse validates:

- Worker approved
- Compliance Passport valid
- Site active
- Required certifications
- Worker not suspended
- Site capacity
- No conflicting assignments

---

## Step 5 — Assignment Activation

Once approved:

Worker receives:

- Site Access
- Attendance Permission
- Safety Package
- Emergency Information
- Site Notifications

---

## Step 6 — Assignment Monitoring

Throughout the assignment:

ConstructPulse continuously monitors:

- Attendance
- Certification Expiry
- Safety Compliance
- Assignment Duration
- Site Transfers

---

## Step 7 — Assignment Completion

Assignments may end because of:

- Project completion
- Manual removal
- Worker transfer
- Employment termination
- Contract completion

Historical records remain permanently available.

---

# Assignment Types

ConstructPulse supports multiple assignment models.

---

## Permanent Assignment

Worker belongs to the site until manually removed.

---

## Temporary Assignment

Worker is assigned for a fixed duration.

Assignment automatically expires.

---

## Multi-Site Assignment

Worker belongs to multiple active sites.

Attendance is only allowed at the site currently occupied.

---

## Emergency Assignment

Temporary assignment during emergency workforce shortages.

Requires elevated approval.

---

# Business Rules

- Workers may belong to multiple sites.
- Workers may only be actively checked into one site at a time.
- Assignment dates determine attendance eligibility.
- Archived sites cannot receive assignments.
- Compliance Passport must remain valid.

---

# Validation Rules

ConstructPulse validates:

✓ Worker Exists

✓ Site Exists

✓ Assignment Dates

✓ Compliance Passport

✓ Site Capacity

✓ Required Certifications

✓ Worker Status

✓ Employer

---

# Failure Scenarios

Examples include:

- Invalid site
- Expired certification
- Worker suspended
- Site inactive
- Assignment overlap
- Site capacity exceeded
- Invalid assignment dates

---

# Audit Events

ConstructPulse records:

- Worker Assigned
- Assignment Updated
- Assignment Removed
- Assignment Expired
- Site Transfer Started
- Site Transfer Completed

---

# Notifications

Workers receive:

- Assignment Created
- Assignment Updated
- Assignment Ending
- Assignment Removed

Managers receive:

- New Worker Assigned
- Assignment Expiring
- Workforce Capacity Alerts

---

# Production Considerations

Supports:

- Unlimited construction sites
- Unlimited workforce
- Temporary labour
- Multi-company projects
- Multiple subcontractors
- Workforce forecasting
- Site capacity management

---

# Future Enhancements

Future releases may support:

- AI workforce scheduling
- Automatic labour balancing
- Skill-based assignment recommendations
- Travel-time optimization
- Fatigue management
- Workforce demand forecasting

# 6.8 QR Attendance, GPS Verification & Site Access Workflow

## Overview

The QR Attendance, GPS Verification & Site Access Workflow is responsible for securely validating worker attendance at construction sites.

Attendance is not determined solely by scanning a QR Code.

ConstructPulse performs multiple validation checks before allowing attendance to be recorded, ensuring workers are physically present, authorized, compliant, and assigned to the selected construction site.

This layered validation prevents attendance fraud, improves workforce visibility, and strengthens site security.

---

# Objectives

This workflow is designed to:

- Verify worker identity
- Confirm physical site presence
- Validate GPS location
- Prevent fraudulent attendance
- Prevent duplicate check-ins
- Support multi-site operations
- Maintain accurate attendance history
- Provide real-time workforce visibility

---

# Actors

Primary Actor

- Worker

Secondary Actors

- Site Manager
- Operations Manager
- Company Administrator

---

# Preconditions

Before attendance begins:

- Worker Approved
- Compliance Passport Valid
- Assigned to Site
- Site Active
- GPS Permission Granted
- Camera Permission Granted
- Safety Induction Completed

---

# Attendance Workflow

## Step 1 — Launch Attendance

Worker opens ConstructPulse.

The application verifies:

- Active session
- Worker status
- Compliance Passport

Only eligible workers may continue.

---

## Step 2 — Scan Site QR Code

Worker scans the site's official QR Code.

ConstructPulse validates:

- QR authenticity
- QR signature
- QR expiration
- Site existence
- Company ownership

Invalid QR codes are immediately rejected.

---

## Step 3 — GPS Verification

ConstructPulse retrieves the worker's current GPS coordinates.

The platform compares:

Worker Location

↓

Site Coordinates

↓

Configured Attendance Radius

Attendance is only permitted if the worker is physically located within the approved geofence.

---

## Step 4 — Workforce Validation

ConstructPulse validates:

✓ Worker Approved

✓ Worker Assigned

✓ Site Active

✓ Compliance Passport Valid

✓ Safety Induction Complete

✓ Required Certifications Valid

✓ Not Suspended

---

## Step 5 — Existing Attendance Check

ConstructPulse checks whether the worker:

- Is already checked into another site
- Has already checked into this site
- Has already checked out
- Has overlapping attendance records

Duplicate attendance is prohibited.

---

## Step 6 — Attendance Creation

If every validation succeeds:

ConstructPulse records:

- Worker
- Site
- Employer
- Trade
- Check-In Time
- GPS Coordinates
- Device Information
- QR Identifier

---

## Step 7 — Dashboard Updates

Immediately after attendance:

The platform updates:

- Live Occupancy
- Workforce Dashboard
- Site Capacity
- Emergency Muster
- Attendance Reports

Updates occur in real time.

---

## Step 8 — Check-Out

When leaving the site:

Worker scans the site QR again or selects Check-Out.

ConstructPulse records:

- Check-Out Time
- GPS Coordinates
- Working Duration

If the worker intends to move to another site, the Site Transfer Workflow begins.

---

# Attendance Validation Engine

Attendance is approved only when every validation succeeds.

```

Worker Logged In

↓

Compliance Passport Valid

↓

Site Assigned

↓

QR Valid

↓

GPS Inside Geofence

↓

No Existing Check-In

↓

Attendance Created

↓

Live Dashboards Updated

```

If any validation fails, attendance is denied.

---

# Business Rules

- Workers may only be checked into one site at a time.
- GPS validation is mandatory.
- QR codes cannot be reused across sites.
- Attendance outside the configured radius is rejected.
- Attendance cannot be manually edited without authorization.
- Archived sites cannot receive attendance.

---

# Validation Rules

ConstructPulse validates:

✓ Worker Status

✓ Compliance Passport

✓ Site Assignment

✓ QR Authenticity

✓ GPS Location

✓ Site Status

✓ Existing Attendance

✓ Device Authentication (Future)

---

# Failure Scenarios

Examples include:

- GPS disabled
- GPS spoofing detected
- Worker outside geofence
- Invalid QR
- QR expired
- Site inactive
- Worker suspended
- Worker not assigned
- Duplicate attendance
- Network interruption

---

# Audit Events

The following events are recorded:

- QR Scanned
- GPS Verified
- Attendance Approved
- Attendance Rejected
- Check-In Completed
- Check-Out Completed
- Validation Failure

---

# Notifications

Worker

- Check-In Successful
- Check-Out Successful
- Attendance Rejected

Site Manager

- Live Workforce Updated
- Capacity Threshold Reached
- Attendance Exception

---

# Production Considerations

Supports:

- Multi-site attendance
- Offline attendance queue (Future)
- GPS geofencing
- Secure QR validation
- Live workforce monitoring
- Large-scale workforce operations

---

# Future Enhancements

Future releases may support:

- NFC attendance
- Bluetooth Beacon validation
- Face verification
- Biometric attendance
- Wearable device integration
- Automatic geofence check-in
- Offline QR verification
- AI fraud detection

# 6.9 Site Transfer & Multi-Site Workforce Movement Workflow

## Overview

The Site Transfer & Multi-Site Workforce Movement Workflow manages the controlled movement of workers between construction sites during the working day.

Construction personnel frequently move between multiple project locations to complete inspections, supervise subcontractors, perform specialist work, or respond to operational requirements.

ConstructPulse ensures that workforce movement is accurately tracked while preventing duplicate attendance, maintaining compliance, and preserving a complete operational history.

Every transfer becomes part of the worker's permanent workforce timeline.

---

# Objectives

The workflow is designed to:

- Support multiple active construction sites
- Prevent duplicate attendance
- Track workforce movement
- Maintain accurate payroll records
- Improve workforce visibility
- Strengthen emergency mustering
- Produce accurate operational analytics

---

# Actors

Primary Actors

- Worker

Secondary Actors

- Site Manager
- Operations Manager
- Company Administrator

---

# Preconditions

Before a transfer begins:

- Worker currently checked into a site.
- Destination site assignment exists.
- Compliance Passport valid.
- Destination site active.
- GPS available.

---

# Site Transfer Workflow

## Step 1 — Active Site Detection

ConstructPulse identifies the worker's current active site.

Information displayed includes:

- Current Site
- Check-In Time
- Time On Site
- Supervisor
- Current Shift

---

## Step 2 — Select Destination Site

Worker selects the destination site.

Available sites include only:

- Assigned Sites
- Active Sites
- Sites with valid permissions

---

## Step 3 — Validate Destination

ConstructPulse verifies:

- Site exists
- Worker assigned
- Site active
- Compliance Passport valid
- Required inductions completed
- Required certifications valid

---

## Step 4 — Check-Out Current Site

The worker checks out of the current site.

ConstructPulse records:

- Check-Out Time
- GPS Coordinates
- Total Working Duration
- Transfer Reason (Optional)

Emergency Muster updates immediately.

---

## Step 5 — Travel Period

ConstructPulse marks the worker as:

"In Transit"

The worker is temporarily removed from the previous site's live occupancy while remaining visible within operational dashboards.

---

## Step 6 — Arrival Verification

Upon arriving at the destination site:

Worker scans the destination QR Code.

ConstructPulse performs:

- GPS Validation
- QR Validation
- Site Assignment Validation
- Compliance Validation

---

## Step 7 — New Site Check-In

ConstructPulse creates a new attendance record.

Information recorded includes:

- Site
- Check-In Time
- GPS Coordinates
- Device Information
- Employer
- Trade

The worker now becomes active at the destination site.

---

## Step 8 — Dashboard Synchronization

The platform immediately updates:

- Previous Site Occupancy
- New Site Occupancy
- Emergency Muster
- Workforce Dashboard
- Attendance Reports
- Workforce Allocation Board

---

# Transfer Types

ConstructPulse supports multiple transfer scenarios.

---

## Planned Transfer

Scheduled movement between projects.

---

## Temporary Assignment

Short-duration work at another site.

---

## Emergency Deployment

Urgent movement to another construction site.

Requires elevated approval.

---

## Permanent Relocation

Worker permanently reassigned.

Historical assignment remains preserved.

---

# Business Rules

- Workers may only be active at one site simultaneously.
- GPS validation is required at every check-in.
- Previous attendance must be closed before the next begins.
- Transfers are permanently recorded.
- Emergency deployments require authorization.

---

# Validation Rules

ConstructPulse validates:

✓ Current Attendance Exists

✓ Destination Site Active

✓ Worker Assigned

✓ Compliance Passport

✓ GPS Validation

✓ QR Validation

✓ Required Inductions

✓ Certifications

---

# Failure Scenarios

Examples include:

- Destination site inactive
- Worker not assigned
- GPS outside geofence
- Duplicate attendance
- Invalid QR
- Compliance expired
- Missing induction

---

# Audit Events

Every transfer records:

- Transfer Started
- Previous Site Check-Out
- Travel Started
- Destination Validation
- New Site Check-In
- Transfer Completed

---

# Notifications

Worker

- Transfer Started
- Arrival Confirmed
- Transfer Completed

Managers

- Worker Left Site
- Worker Arrived
- Workforce Allocation Updated

---

# Production Considerations

Supports:

- Unlimited daily transfers
- Multi-project operations
- Regional workforce movement
- Live occupancy updates
- Real-time emergency mustering
- Payroll segmentation by site

---

# Future Enhancements

Future releases may support:

- Route optimization
- Travel time estimation
- Automatic GPS transfer detection
- Fleet vehicle integration
- AI workforce redistribution

# 6.10 Emergency Management & Digital Muster Workflow

## Overview

The Emergency Management & Digital Muster Workflow enables construction companies to rapidly account for every worker during an emergency event.

When an emergency is declared, ConstructPulse immediately freezes workforce movement, captures the current workforce state, and provides real-time visibility into personnel across all construction sites.

The objective is to enable rapid accountability, improve emergency response, and support health & safety compliance.

---

# Objectives

The workflow is designed to:

- Account for every worker
- Improve emergency response
- Reduce evacuation time
- Identify missing personnel
- Assist emergency services
- Maintain incident history
- Support regulatory compliance

---

# Actors

Primary Actors

- Site Manager
- Safety Officer

Secondary Actors

- Operations Manager
- Company Administrator
- Emergency Responders
- Worker

---

# Preconditions

Before emergency activation:

- Site Active
- Workers Checked In
- Emergency Contacts Configured
- Muster Point Configured

---

# Emergency Workflow

## Step 1 — Emergency Declared

An authorized person declares an emergency.

Emergency types may include:

- Fire
- Medical Emergency
- Structural Failure
- Gas Leak
- Severe Weather
- Earthquake
- Security Threat
- Other

The incident immediately becomes active.

---

## Step 2 — Attendance Freeze

ConstructPulse temporarily freezes attendance changes.

Current workforce data is locked.

The platform records:

- Workers On Site
- Workers In Transit
- Visitors
- Contractors
- Site Managers

---

## Step 3 — Emergency Notifications

Notifications are immediately sent.

Workers receive:

- Emergency Alert
- Evacuation Instructions
- Muster Point

Managers receive:

- Live Workforce Status
- Missing Worker Count
- Emergency Dashboard

---

## Step 4 — Evacuation

Workers proceed to the designated muster point.

ConstructPulse displays:

- Muster Point Map
- Emergency Contacts
- Evacuation Route
- Safety Instructions

---

## Step 5 — Digital Muster

At the assembly point:

Workers confirm they are safe.

Confirmation methods may include:

- QR Scan
- NFC
- Manual Confirmation
- Supervisor Confirmation

ConstructPulse updates the worker's emergency status in real time.

---

## Step 6 — Live Accountability

The Emergency Dashboard categorizes personnel.

Safe

Workers confirmed at the muster point.

Missing

Workers not yet accounted for.

In Transit

Workers moving between sites.

Off Site

Workers previously checked out.

Visitors

Visitors currently on site.

Emergency Responders

Personnel assisting with the incident.

---

## Step 7 — Missing Worker Investigation

For every missing worker ConstructPulse displays:

- Last Check-In Time
- Last GPS Location
- Last Assigned Site
- Supervisor
- Employer
- Trade
- Emergency Contact
- Recent Activity Timeline

This information assists emergency responders.

---

## Step 8 — Incident Resolution

When the emergency concludes:

ConstructPulse records:

- Resolution Time
- Incident Summary
- Final Muster Report
- Attendance Restoration

Normal operations resume.

---

# Business Rules

- Only authorized users may declare emergencies.
- Attendance freezes during an active emergency.
- Every emergency generates an incident report.
- Muster confirmations are permanently recorded.
- Missing workers remain highlighted until resolved.

---

# Validation Rules

ConstructPulse validates:

✓ Emergency Active

✓ Worker Identity

✓ Site Association

✓ Muster Confirmation

✓ Incident Status

---

# Failure Scenarios

Examples include:

- Worker unable to respond
- GPS unavailable
- QR unavailable
- Communication failure
- Network interruption

---

# Audit Events

Every emergency action is recorded.

Examples include:

- Emergency Declared
- Notifications Sent
- Muster Started
- Worker Confirmed Safe
- Worker Marked Missing
- Incident Closed

---

# Notifications

Workers

- Emergency Alert
- Muster Reminder
- Incident Closed

Managers

- Emergency Activated
- Worker Missing
- Muster Complete

Emergency Responders

- Workforce Manifest
- Missing Worker List
- Incident Summary

---

# Production Considerations

Supports:

- Multi-site emergencies
- Simultaneous incidents
- Live dashboards
- Large workforce accountability
- Offline emergency procedures (Future)

---

# Future Enhancements

Future releases may include:

- SOS Button
- Satellite messaging
- Smartwatch integration
- Automatic fall detection
- Wearable panic buttons
- Drone-assisted evacuation
- AI emergency coordination

# 6.11 Subcontractor Company & Workforce Management Workflow

## Overview

The Subcontractor Company & Workforce Management Workflow enables Limelite Construction to manage external subcontractor organizations alongside its internal workforce.

Each subcontractor company maintains its own workforce while operating under Limelite's compliance, attendance, and safety requirements.

ConstructPulse provides complete visibility into subcontractor activities without compromising organizational control.

---

# Objectives

The workflow is designed to:

- Register subcontractor companies
- Manage subcontractor workers
- Assign subcontractors to projects
- Track workforce ownership
- Monitor subcontractor performance
- Enforce safety compliance
- Maintain contractual accountability

---

# Actors

Primary Actors

- Company Administrator
- Operations Manager

Secondary Actors

- Site Manager
- Subcontractor Manager

---

# Preconditions

Before subcontractor onboarding:

- Limelite company exists
- Subcontractor approved
- Contract established
- Required insurance verified (Optional)
- Required documentation uploaded

---

# Workflow

## Step 1 — Register Subcontractor Company

Administrator creates a subcontractor profile.

Information includes:

- Company Name
- NZBN
- Contact Person
- Mobile Number
- Email
- Business Address
- Company Logo
- Primary Trade
- Contract Period

---

## Step 2 — Configure Company Profile

ConstructPulse records:

- Services Offered
- Trade Categories
- Number of Workers
- Insurance Details
- Compliance Documents
- Health & Safety Rating
- Preferred Sites

---

## Step 3 — Assign Company to Projects

Administrator assigns the subcontractor company to one or more construction sites.

Assignment includes:

- Project
- Start Date
- End Date
- Contract Scope
- Maximum Workforce

---

## Step 4 — Worker Registration

Workers register normally.

During registration they select:

Employer

↓

ABC Electrical Ltd

instead of

Limelite Construction.

---

## Step 5 — Approval

Approval follows the configured workflow.

ConstructPulse links every worker to:

Employer

↓

Project

↓

Trade

↓

Site

---

## Step 6 — Workforce Monitoring

ConstructPulse tracks:

- Active Workers
- Attendance
- Compliance
- Site Allocation
- Incident History
- Workforce Hours

---

## Step 7 — Performance Monitoring

Managers review:

- Attendance Rate
- Safety Compliance
- Incident Count
- Workforce Availability
- Project Contribution

---

## Step 8 — Contract Completion

When the subcontract ends:

- Workers removed from future assignments
- Historical records retained
- Company archived (optional)

---

# Business Rules

- Every worker belongs to exactly one employer.
- Employers may work on multiple sites.
- Multiple subcontractors may share the same project.
- Internal employees and subcontractors follow identical safety requirements.
- Subcontractors cannot access other subcontractors' information.

---

# Validation Rules

ConstructPulse validates:

✓ Company Exists

✓ Active Contract

✓ Site Assignment

✓ Worker Association

✓ Compliance Status

---

# Failure Scenarios

Examples include:

- Expired contract
- Missing insurance
- Invalid assignment
- Company suspended
- Worker linked to incorrect employer

---

# Audit Events

ConstructPulse records:

- Company Registered
- Contract Started
- Worker Assigned
- Worker Removed
- Company Archived

---

# Notifications

Subcontractor Manager

- Worker Registered
- Worker Approved
- Compliance Expired

Operations Manager

- Workforce Shortage
- Contract Expiring
- Compliance Alerts

---

# Production Considerations

Supports:

- Unlimited subcontractor companies
- Multi-project contracts
- Regional operations
- Workforce sharing
- Historical reporting

---

# Future Enhancements

Future releases may include:

- Contract Management
- Insurance Tracking
- Invoice Integration
- Timesheet Export
- Performance Scorecards
- Digital Purchase Orders

# 6.12 Operations Dashboard, Reporting & Analytics Workflow

## Overview

The Operations Dashboard & Reporting Workflow provides real-time visibility into workforce operations across the entire organization.

Rather than presenting raw attendance records, ConstructPulse transforms operational data into actionable insights for executives, operations managers, site managers, and supervisors.

The dashboard acts as the central command center for workforce management, construction site monitoring, compliance oversight, and operational decision-making.

---

# Objectives

The workflow is designed to:

- Monitor workforce operations
- Support executive decision making
- Identify operational risks
- Improve workforce utilization
- Monitor compliance
- Track project progress
- Provide historical analytics

---

# Actors

Primary Actors

- Company Director
- Operations Manager

Secondary Actors

- Company Administrator
- Site Manager
- Safety Officer

---

# Dashboard Structure

ConstructPulse provides multiple dashboards depending on user responsibilities.

---

## Executive Dashboard

Provides organization-wide visibility.

Displays:

- Total Workforce
- Active Projects
- Active Construction Sites
- Live Workforce
- Attendance Rate
- Compliance Percentage
- Open Incidents
- Pending Approvals
- Labour Utilization
- Workforce Capacity
- Site Performance

---

## Operations Dashboard

Focuses on daily operations.

Displays:

- Workforce Allocation
- Site Occupancy
- Site Transfers
- Attendance Exceptions
- Late Check-ins
- Missing Workers
- GPS Exceptions
- QR Validation Failures
- Site Capacity Alerts

---

## Site Manager Dashboard

Displays information only for assigned sites.

Includes:

- Workers On Site
- Visitors
- Contractors
- Attendance
- Toolbox Talks
- Safety Alerts
- Open Incidents
- Daily Site Activity

---

## Safety Dashboard

Displays:

- Safety Compliance
- Missing Inductions
- Expired Certifications
- Active Incidents
- Near Miss Reports
- Emergency Muster Status
- High Risk Workers

---

## Workforce Dashboard

Displays:

- Active Workers
- Workers by Employer
- Workers by Trade
- Workforce Distribution
- Temporary Assignments
- Transfer Activity
- Workforce Availability

---

# Operational Reports

ConstructPulse generates:

Attendance Reports

Compliance Reports

Labour Reports

Subcontractor Reports

Safety Reports

Incident Reports

Emergency Reports

Site Occupancy Reports

GPS Validation Reports

QR Scan Reports

Workforce Allocation Reports

Transfer Reports

Certification Reports

---

# Report Filters

Reports support filtering by:

- Date Range
- Site
- Worker
- Employer
- Trade
- Department
- Supervisor
- Site Manager
- Project
- Attendance Status
- Compliance Status

---

# Live Monitoring

Dashboards update in real time.

Examples include:

- New Attendance
- Worker Checkout
- Site Transfer
- Emergency Activation
- Incident Reports
- Compliance Changes

---

# Business Rules

- Dashboard visibility depends on user permissions.
- Managers only view assigned sites.
- Directors view organization-wide information.
- Historical data remains immutable.
- Reports may be exported.

---

# Validation Rules

ConstructPulse validates:

✓ User Permission

✓ Company Scope

✓ Site Assignment

✓ Report Filters

✓ Data Availability

---

# Failure Scenarios

Examples include:

- Insufficient permissions
- Invalid report filters
- Archived projects
- Data unavailable

---

# Audit Events

ConstructPulse records:

- Report Generated
- Report Exported
- Dashboard Accessed
- Filter Applied
- Analytics Viewed

---

# Notifications

Dashboard alerts include:

- Workforce Shortages
- Compliance Risks
- Site Capacity Alerts
- Certification Expiry
- Emergency Incidents
- Approval Backlog
- Missing Workers

---

# Production Considerations

Supports:

- Real-time dashboards
- Multi-company reporting
- Large workforce analytics
- Historical trend analysis
- Export to PDF
- Export to Excel
- Scheduled reports

---

# Future Enhancements

Future releases may include:

- AI workforce forecasting
- Labour cost prediction
- Project delay prediction
- Executive KPI scorecards
- Custom dashboard builder
- Natural language reporting

# 6.13 Compliance Passport, Certifications & Training Workflow

## Overview

The Compliance Passport & Certification Workflow ensures that every worker entering a construction site satisfies the company's health, safety, regulatory, and competency requirements.

Rather than relying on manual spreadsheets or paper records, ConstructPulse maintains a live digital compliance profile for every worker.

The platform continuously validates certifications, training records, inductions, licenses, and mandatory qualifications before allowing workers to access construction sites.

This workflow significantly reduces compliance risk while simplifying workforce management.

---

# Objectives

The workflow is designed to:

- Maintain worker compliance
- Track certifications
- Monitor training completion
- Prevent expired qualifications
- Improve site safety
- Support regulatory audits
- Simplify compliance reporting

---

# Actors

Primary Actors

- Worker

Secondary Actors

- Safety Officer
- Site Manager
- Operations Manager
- Company Administrator

---

# Preconditions

Before compliance validation:

- Worker registered
- Worker approved
- Worker assigned to employer
- Compliance requirements configured

---

# Compliance Passport

Every worker receives a Digital Compliance Passport.

The passport contains:

- Worker Identity
- Employer
- Trade
- Employment Status
- Assigned Sites
- Required Certifications
- Completed Inductions
- Medical Requirements (optional)
- Emergency Contacts
- Compliance Status

---

# Certification Management

ConstructPulse tracks certifications including:

- Site Safety Induction
- General Construction Safety
- Working at Heights
- Confined Space Entry
- Elevated Work Platform
- Scaffolding
- Crane Operations
- Forklift License
- Electrical License
- First Aid
- Fire Warden
- Traffic Management
- Hazardous Materials
- Any custom certification

Administrators can configure additional certification types.

---

# Training Workflow

## Step 1 — Certification Added

A certification is uploaded or assigned.

Information includes:

- Certification Type
- Certificate Number
- Issuing Organization
- Issue Date
- Expiry Date
- Supporting Documents

---

## Step 2 — Validation

ConstructPulse validates:

- Certificate exists
- Dates valid
- Worker assigned
- Document uploaded (optional)

---

## Step 3 — Compliance Evaluation

ConstructPulse evaluates:

✓ Mandatory certifications

✓ Site-specific requirements

✓ Trade-specific requirements

✓ Employer requirements

✓ Regulatory requirements

---

## Step 4 — Compliance Status

Workers are classified as:

🟢 Fully Compliant

🟡 Expiring Soon

🔴 Non-Compliant

---

## Step 5 — Attendance Integration

Before every check-in:

ConstructPulse validates:

- Compliance Passport
- Site Requirements
- Mandatory Training

Workers failing compliance cannot enter the site.

---

# Business Rules

- Expired certifications immediately affect compliance.
- Site-specific certifications override general requirements.
- Mandatory inductions must be completed before first attendance.
- Historical certifications remain archived.
- Custom certification templates are supported.

---

# Validation Rules

ConstructPulse validates:

✓ Certificate Expiry

✓ Mandatory Training

✓ Site Requirements

✓ Worker Trade

✓ Employer Rules

---

# Failure Scenarios

Examples include:

- Expired certificate
- Missing induction
- Missing trade qualification
- Invalid documentation
- Site-specific requirement not met

---

# Audit Events

ConstructPulse records:

- Certification Added
- Certification Updated
- Certification Expired
- Training Completed
- Compliance Status Changed

---

# Notifications

Workers receive:

- Certification Expiring
- Training Required
- Compliance Restored

Managers receive:

- Expired Certifications
- Workforce Compliance Alerts
- Site Compliance Risks

---

# Production Considerations

Supports:

- Unlimited certification types
- Company-specific compliance rules
- Site-specific requirements
- Automatic expiry monitoring
- Regulatory audit support

---

# Future Enhancements

Future releases may include:

- OCR certificate verification
- Government license verification
- Digital certificate wallet
- Auto-renewal reminders
- External LMS integration
- AI compliance risk prediction

# 6.14 Visitor, Client & Guest Management Workflow

## Overview

The Visitor, Client & Guest Management Workflow enables ConstructPulse to securely manage every non-worker entering a construction site.

Visitors do not participate in workforce attendance but must still be tracked for safety, emergency mustering, compliance, and auditing purposes.

Every visitor receives a temporary digital visitor profile and is associated with a host, construction site, and visit purpose.

This workflow ensures complete visibility of everyone present on-site at any given time.

---

# Objectives

The workflow is designed to:

- Register visitors
- Track site access
- Improve site security
- Support emergency mustering
- Maintain visitor history
- Reduce manual paperwork
- Improve compliance

---

# Actors

Primary Actors

- Visitor
- Site Manager
- Site Administrator

Secondary Actors

- Reception
- Security Guard
- Host Employee
- Safety Officer

---

# Visitor Types

ConstructPulse supports multiple visitor categories.

Examples include:

- Client
- Architect
- Engineer
- Consultant
- Council Inspector
- Government Inspector
- Delivery Driver
- Equipment Supplier
- Maintenance Technician
- Job Applicant
- Auditor
- General Visitor

Administrators may configure additional visitor categories.

---

# Preconditions

Before site entry:

- Site active
- Host selected
- Visit purpose entered
- Safety acknowledgement accepted
- Emergency contact available (optional)

---

# Visitor Workflow

## Step 1 — Visitor Registration

Visitor enters:

- Full Name
- Company
- Mobile Number
- Email (optional)
- Vehicle Registration (optional)
- Visit Purpose

---

## Step 2 — Host Selection

Visitor selects or is assigned:

- Host Employee
- Site Manager
- Project Manager

The host receives an approval notification.

---

## Step 3 — Safety Acknowledgement

Before entry ConstructPulse presents:

- Site Rules
- PPE Requirements
- Emergency Procedures
- Muster Point
- Restricted Areas

Visitor confirms acknowledgement.

---

## Step 4 — QR Visitor Pass

ConstructPulse generates a temporary Visitor Pass.

The pass contains:

- Visitor Name
- Company
- Host
- Site
- Check-In Time
- Expiry Time
- QR Identifier

---

## Step 5 — Site Entry

Visitor scans the Visitor QR.

ConstructPulse records:

- Arrival Time
- GPS Location (optional)
- Device
- Host

Visitor becomes active on-site.

---

## Step 6 — Site Exit

Visitor checks out.

ConstructPulse records:

- Departure Time
- Visit Duration

The Visitor Pass becomes inactive.

---

# Business Rules

- Every visitor must have a host.
- Visitors cannot enter restricted areas without authorization.
- Visitor passes automatically expire.
- Visitor history remains permanently available.

---

# Validation Rules

ConstructPulse validates:

✓ Site Active

✓ Host Exists

✓ Visit Purpose

✓ Visitor Pass Valid

✓ Safety Acknowledgement Completed

---

# Failure Scenarios

Examples include:

- Host unavailable
- Visitor pass expired
- Invalid QR
- Restricted access request
- Safety acknowledgement incomplete

---

# Audit Events

ConstructPulse records:

- Visitor Registered
- Visitor Approved
- Visitor Checked In
- Visitor Checked Out
- Visitor Pass Expired

---

# Notifications

Host receives:

- Visitor Arrived
- Visitor Waiting
- Visitor Checked Out

Site Manager receives:

- Active Visitors
- Visitor Count
- Visitor Overstay Alerts

---

# Production Considerations

Supports:

- Multiple simultaneous visitors
- Multi-site operations
- Visitor history
- Temporary access
- Emergency mustering

---

# Future Enhancements

Future releases may include:

- Digital ID verification
- Facial recognition
- Driver's license scanning
- Vehicle gate integration
- Visitor self-service kiosk

# 6.15 Incident, Hazard & Near Miss Management Workflow

## Overview

The Incident, Hazard & Near Miss Management Workflow enables ConstructPulse to digitally record, investigate, monitor, and resolve all safety-related events occurring across construction sites.

Rather than relying on paper forms or delayed reporting, every worker can immediately report incidents directly from the mobile application.

The workflow promotes proactive safety management by capturing hazards before they become accidents while maintaining complete regulatory records for investigations and compliance audits.

---

# Objectives

The workflow is designed to:

- Report workplace incidents
- Capture near misses
- Identify hazards
- Improve safety culture
- Reduce workplace injuries
- Maintain legal compliance
- Support incident investigations

---

# Actors

Primary Actors

- Worker
- Site Manager
- Safety Officer

Secondary Actors

- Operations Manager
- Company Administrator
- Director

---

# Incident Categories

ConstructPulse supports multiple incident categories.

Examples include:

- Injury
- Near Miss
- Hazard Observation
- Unsafe Behaviour
- Unsafe Condition
- Property Damage
- Environmental Incident
- Equipment Failure
- Vehicle Accident
- Security Incident

Administrators may configure additional categories.

---

# Severity Levels

Every incident receives a severity rating.

Levels include:

🟢 Low

🟡 Medium

🟠 High

🔴 Critical

Severity determines escalation requirements.

---

# Preconditions

Before submitting an incident:

- Worker authenticated
- Worker assigned to site
- Site active

Visitors may also be reported.

---

# Incident Workflow

## Step 1 — Create Incident

Reporter selects:

- Incident Type
- Site
- Location
- Date & Time
- Severity

---

## Step 2 — Describe Event

Reporter provides:

- Description
- What happened
- Immediate actions taken
- Persons involved

---

## Step 3 — Attach Evidence

Optional attachments include:

- Photos
- Videos
- Documents
- Voice Notes

---

## Step 4 — Hazard Identification

Reporter identifies:

- Immediate Hazard
- Potential Consequences
- Area Affected

---

## Step 5 — Initial Notification

ConstructPulse immediately notifies:

- Site Manager
- Safety Officer

Critical incidents additionally notify:

- Operations Manager
- Director

---

## Step 6 — Investigation

Safety Officer records:

- Root Cause
- Contributing Factors
- Corrective Actions
- Preventive Actions

---

## Step 7 — Corrective Actions

Actions may include:

- Toolbox Talk
- Equipment Repair
- Worker Retraining
- Site Closure
- Engineering Controls
- Procedure Updates

Each action receives:

- Responsible Person
- Due Date
- Completion Status

---

## Step 8 — Incident Closure

Once all actions are complete:

Incident status changes to:

Closed

Historical records remain immutable.

---

# Business Rules

- Critical incidents require immediate escalation.
- Every incident receives a unique reference number.
- Closed incidents cannot be deleted.
- Evidence remains permanently archived.
- Corrective actions must be tracked until completion.

---

# Validation Rules

ConstructPulse validates:

✓ Site Exists

✓ Reporter Exists

✓ Incident Category

✓ Severity

✓ Mandatory Description

---

# Failure Scenarios

Examples include:

- Missing description
- Invalid site
- Invalid severity
- Duplicate report
- Upload failure

---

# Audit Events

ConstructPulse records:

- Incident Created
- Evidence Uploaded
- Investigation Started
- Corrective Action Assigned
- Incident Closed

---

# Notifications

Workers receive:

- Incident Submitted
- Investigation Update
- Incident Closed

Managers receive:

- Critical Incident Alert
- Investigation Assigned
- Corrective Action Overdue

---

# Production Considerations

Supports:

- Unlimited incidents
- Multi-site investigations
- Photo evidence
- Root cause analysis
- Corrective action tracking
- Regulatory reporting

---

# Future Enhancements

Future releases may include:

- AI hazard classification
- Automatic risk scoring
- OCR document extraction
- Voice-to-text reporting
- Integration with national workplace safety systems

# 6.16 Communication, Announcements & Toolbox Talk Workflow

## Overview

The Communication, Announcements & Toolbox Talk Workflow provides a centralized platform for delivering important operational updates, safety communications, toolbox talks, emergency notices, and company announcements.

Every worker receives the right information at the right time based on their assigned company, project, trade, and construction site.

ConstructPulse ensures that critical safety information is acknowledged before work begins, improving communication, compliance, and workforce awareness.

---

# Objectives

The workflow is designed to:

- Deliver daily toolbox talks
- Share company announcements
- Publish site instructions
- Communicate emergency notices
- Improve workforce awareness
- Maintain acknowledgement records
- Reduce communication gaps

---

# Actors

Primary Actors

- Site Manager
- Safety Officer

Secondary Actors

- Operations Manager
- Company Administrator
- Director
- Worker

---

# Communication Categories

ConstructPulse supports:

- Daily Toolbox Talks
- Safety Alerts
- Site Instructions
- Company Announcements
- Emergency Notifications
- Weather Warnings
- Project Updates
- Equipment Notices
- Policy Updates
- Training Announcements

Administrators may configure additional categories.

---

# Preconditions

Before publishing:

- Site selected
- Audience selected
- Valid publisher permissions

---

# Communication Workflow

## Step 1 — Create Announcement

Authorized users create a communication.

Fields include:

- Title
- Category
- Description
- Priority
- Effective Date
- Expiry Date
- Target Audience

---

## Step 2 — Audience Selection

Announcements may target:

- Entire Company
- Specific Site
- Specific Project
- Trade
- Department
- Employer
- Individual Worker
- Visitors

---

## Step 3 — Attach Supporting Material

Optional attachments include:

- PDFs
- Images
- Videos
- Safety Documents
- Drawings
- Procedures
- External Links

---

## Step 4 — Publish

ConstructPulse immediately distributes notifications.

Workers receive push notifications on mobile devices.

---

## Step 5 — Acknowledgement

Certain communications require acknowledgement.

Examples include:

- Site Rules
- Emergency Procedures
- Toolbox Talks
- Safety Bulletins
- High Risk Work Notices

Workers must acknowledge before continuing.

---

## Step 6 — Attendance Integration

When configured as mandatory:

ConstructPulse blocks attendance until the worker has acknowledged the required communication.

Examples:

- Daily Toolbox Talk
- Site Safety Update
- Hazard Notice
- Severe Weather Alert

---

## Step 7 — Monitoring

Managers can monitor:

- Delivered
- Read
- Acknowledged
- Pending
- Expired

Real-time dashboards display acknowledgement percentages.

---

# Toolbox Talk Workflow

Each toolbox talk includes:

- Topic
- Presenter
- Date
- Site
- Duration
- Supporting Documents
- Attendance List
- Worker Acknowledgements

Historical toolbox talks remain searchable.

---

# Business Rules

- Mandatory communications must be acknowledged.
- Expired announcements become read-only.
- Workers only receive communications relevant to them.
- Emergency alerts override all other notifications.

---

# Validation Rules

ConstructPulse validates:

✓ Publisher Permission

✓ Audience

✓ Active Site

✓ Communication Type

✓ Mandatory Flag

---

# Failure Scenarios

Examples include:

- Invalid audience
- Missing title
- Attachment upload failure
- Expired communication
- Duplicate publication

---

# Audit Events

ConstructPulse records:

- Announcement Created
- Announcement Updated
- Published
- Worker Viewed
- Worker Acknowledged
- Announcement Archived

---

# Notifications

Workers receive:

- New Announcement
- Toolbox Talk Available
- Safety Alert
- Emergency Notification

Managers receive:

- Low Acknowledgement Rate
- Expired Communication
- Mandatory Communication Outstanding

---

# Production Considerations

Supports:

- Unlimited announcements
- Multi-site communications
- Multi-language support
- Attachment management
- Push notifications
- Read receipts

---

# Future Enhancements

Future releases may include:

- AI-generated toolbox talks
- Automatic translation
- Voice announcements
- Video toolbox talks
- Interactive safety quizzes
- SMS fallback notifications

# 6.17 Asset, Equipment & Tool Management Workflow

## Overview

The Asset, Equipment & Tool Management Workflow enables ConstructPulse to manage construction equipment, company assets, tools, machinery, and safety equipment across multiple construction sites.

Every asset is uniquely identified, assigned, inspected, maintained, and tracked throughout its lifecycle.

The workflow improves operational efficiency, reduces equipment loss, supports maintenance planning, and strengthens workplace safety.

---

# Objectives

The workflow is designed to:

- Track company assets
- Assign equipment to workers
- Monitor equipment location
- Schedule inspections
- Manage maintenance
- Prevent equipment loss
- Improve asset utilization

---

# Actors

Primary Actors

- Store Manager
- Site Manager

Secondary Actors

- Worker
- Operations Manager
- Company Administrator

---

# Asset Categories

ConstructPulse supports:

Heavy Machinery

- Excavators
- Cranes
- Forklifts
- Loaders

Power Tools

- Drills
- Grinders
- Saws

Safety Equipment

- Harnesses
- Gas Detectors
- Tripods
- Rescue Kits

PPE

- Helmets
- Gloves
- Boots
- Safety Glasses
- Respirators

Vehicles

- Utes
- Trucks
- Vans

Site Equipment

- Generators
- Compressors
- Pumps
- Temporary Lighting

Office Assets

- Tablets
- Phones
- Laptops
- Printers

Administrators may create unlimited custom asset categories.

---

# Preconditions

Before asset allocation:

- Asset registered
- Asset active
- Inspection valid
- Worker approved
- Site active

---

# Asset Lifecycle

## Step 1 — Register Asset

Administrator records:

- Asset ID
- QR Code
- Serial Number
- Category
- Manufacturer
- Purchase Date
- Warranty
- Site
- Current Status

---

## Step 2 — Inspection

ConstructPulse records:

- Inspection Date
- Inspector
- Inspection Result
- Defects
- Photos

Inspection history remains permanent.

---

## Step 3 — Assignment

Asset may be assigned to:

- Worker
- Supervisor
- Site
- Department

Assignment includes:

- Start Time
- Expected Return
- Condition

---

## Step 4 — Usage Tracking

ConstructPulse records:

- Check-Out
- Check-In
- Hours Used
- Operator
- GPS Location (optional)

---

## Step 5 — Maintenance

Maintenance events include:

- Preventive Maintenance
- Repairs
- Calibration
- Replacement Parts

Maintenance schedules are automatically generated.

---

## Step 6 — Retirement

Assets may be:

- Archived
- Sold
- Replaced
- Scrapped

Historical records remain available.

---

# Business Rules

- Assets cannot be assigned twice simultaneously.
- Inspection expiry prevents assignment.
- Damaged equipment cannot be issued.
- Asset history cannot be deleted.

---

# Validation Rules

ConstructPulse validates:

✓ Asset Exists

✓ Asset Available

✓ Inspection Valid

✓ Worker Authorized

✓ Site Assignment

---

# Failure Scenarios

Examples include:

- Asset unavailable
- Inspection expired
- Damaged equipment
- Duplicate assignment
- Maintenance overdue

---

# Audit Events

ConstructPulse records:

- Asset Created
- Asset Assigned
- Asset Returned
- Inspection Completed
- Maintenance Scheduled
- Asset Retired

---

# Notifications

Workers receive:

- Tool Assigned
- Return Reminder

Managers receive:

- Inspection Due
- Maintenance Overdue
- Missing Equipment
- Asset Damage Report

---

# Production Considerations

Supports:

- Unlimited assets
- Multi-site tracking
- QR-based asset identification
- Maintenance scheduling
- Inspection history

---

# Future Enhancements

Future releases may include:

- Bluetooth tracking
- RFID integration
- IoT equipment monitoring
- Fuel monitoring
- Utilization analytics
- Predictive maintenance

# 6.18 System Administration, Configuration & Organization Management Workflow

## Overview

The System Administration & Configuration Workflow enables authorized administrators to configure, customize, and manage every aspect of the ConstructPulse platform.

Rather than embedding business rules directly into the application, ConstructPulse provides configurable administrative controls that allow organizations to adapt the platform to their operational processes without requiring software changes.

The workflow supports organizational management, role administration, security configuration, company settings, site configuration, workflow customization, and platform governance.

---

# Objectives

The workflow is designed to:

- Configure organizational settings
- Manage users and permissions
- Configure construction sites
- Define business rules
- Manage platform security
- Support multi-company environments
- Enable future scalability

---

# Actors

Primary Actors

- System Administrator
- Company Administrator

Secondary Actors

- Director
- Operations Manager
- IT Administrator

---

# Administration Modules

ConstructPulse provides configurable administration modules.

These include:

- Company Management
- Site Management
- User Management
- Role Management
- Permission Management
- Trade Management
- Department Management
- Subcontractor Management
- Compliance Configuration
- Attendance Configuration
- Notification Configuration
- Emergency Configuration
- Document Management
- Asset Configuration
- System Configuration

---

# Company Configuration

Administrators can configure:

- Company Name
- Company Logo
- Company Branding
- Contact Details
- NZBN
- Office Locations
- Time Zone
- Default Language
- Emergency Contacts

---

# Site Configuration

Each construction site supports:

- Site Name
- Project Name
- Address
- GPS Coordinates
- Attendance Radius
- Muster Points
- Site Manager
- Site Status
- Working Hours
- Site Capacity

---

# User Management

Administrators can:

- Create Users
- Disable Users
- Reset Accounts
- Assign Roles
- Change Employers
- Transfer Workers
- Archive Accounts

---

# Role Management

Supported roles include:

- Director
- Operations Manager
- Company Administrator
- Site Manager
- Safety Officer
- Supervisor
- Worker
- Visitor

Organizations may define custom roles.

---

# Permission Engine

Permissions are configurable.

Examples include:

- Create Sites
- Approve Workers
- Manage Attendance
- Declare Emergencies
- Manage Assets
- Publish Announcements
- View Reports
- Export Data

Permissions are assigned through Role-Based Access Control (RBAC).

---

# Compliance Configuration

Administrators define:

- Required Certifications
- Expiry Periods
- Trade Requirements
- Site Requirements
- Induction Requirements
- Compliance Rules

---

# Attendance Configuration

Configurable options include:

- GPS Radius
- QR Expiry
- Shift Rules
- Early Check-In Window
- Late Check-In Threshold
- Automatic Check-Out
- Overtime Rules

---

# Notification Configuration

Organizations configure:

- Push Notifications
- Email Notifications
- SMS Notifications (Future)
- Emergency Broadcasts
- Reminder Schedules

---

# Branding Configuration

Organizations may customize:

- Logo
- App Name
- Primary Colors
- Welcome Screen
- Login Screen
- Company Documents

---

# Business Rules

- Configuration changes require administrator permission.
- Company data remains isolated.
- Every configuration change is audited.
- Archived configurations remain recoverable.

---

# Validation Rules

ConstructPulse validates:

✓ Administrator Permission

✓ Configuration Completeness

✓ Data Integrity

✓ Company Scope

---

# Failure Scenarios

Examples include:

- Invalid configuration
- Missing mandatory settings
- Duplicate roles
- Invalid permission assignment
- Configuration conflicts

---

# Audit Events

ConstructPulse records:

- Setting Changed
- Role Created
- Permission Updated
- Company Updated
- Site Configured
- Workflow Modified

---

# Notifications

Administrators receive:

- Configuration Changes
- Security Alerts
- Permission Changes
- Failed Login Attempts

---

# Production Considerations

Supports:

- Unlimited companies
- Unlimited sites
- Unlimited roles
- Unlimited configuration templates
- Future feature toggles

---

# Future Enhancements

Future releases may include:

- White-label deployments
- Multi-region support
- Multi-language localization
- API configuration portal
- Feature flag management
- Enterprise SSO (Azure AD, Okta, Google Workspace)

# 6.19 Audit Logs, Security & Compliance History Workflow

## Overview

The Audit Logs, Security & Compliance History Workflow provides complete traceability of all activities performed within ConstructPulse.

Every important action performed by users, administrators, system services, and automated workflows is permanently recorded.

These audit records ensure accountability, strengthen security, support regulatory compliance, and assist with investigations, incident analysis, and operational reviews.

Audit records are immutable and form the official history of the platform.

---

# Objectives

The workflow is designed to:

- Record every critical system action
- Improve accountability
- Support compliance audits
- Strengthen security
- Investigate incidents
- Monitor administrative activity
- Maintain historical records

---

# Actors

Primary Actors

- System Administrator
- Company Administrator

Secondary Actors

- Director
- Operations Manager
- Security Officer
- Compliance Officer

---

# Audit Categories

ConstructPulse records activities across multiple categories.

These include:

Authentication

- Login
- Logout
- Failed Login
- Password Reset
- Session Expiry

User Management

- User Created
- User Approved
- User Rejected
- Role Changed
- Account Disabled

Attendance

- Check-In
- Check-Out
- GPS Validation
- QR Scan
- Attendance Override

Site Management

- Site Created
- Site Updated
- Site Archived
- Site Assignment

Compliance

- Certification Added
- Certification Updated
- Certification Expired
- Induction Completed

Emergency

- Emergency Declared
- Muster Started
- Muster Completed
- Emergency Closed

Incident Management

- Incident Created
- Investigation Started
- Corrective Action Completed

Assets

- Asset Assigned
- Asset Returned
- Maintenance Scheduled

Administration

- Permission Changed
- Configuration Updated
- Workflow Modified
- Feature Enabled
- Feature Disabled

---

# Audit Workflow

## Step 1 — Action Occurs

A user or system performs an action.

Example:

Worker Approved

---

## Step 2 — Audit Event Generated

ConstructPulse immediately creates an audit record.

---

## Step 3 — Metadata Collection

Each audit event records:

- Timestamp
- User
- User Role
- Company
- Site
- Device
- IP Address
- GPS (where applicable)
- Module
- Action
- Previous Value
- New Value

---

## Step 4 — Secure Storage

Audit events are stored in an immutable audit repository.

Records cannot be modified or deleted through the application.

---

## Step 5 — Monitoring

Security dashboards continuously monitor:

- Unusual login attempts
- Excessive failed logins
- Permission changes
- Large data exports
- Suspicious administrator activity

---

## Step 6 — Investigation

Authorized personnel can search audit logs using filters such as:

- Date Range
- User
- Company
- Site
- Action Type
- Module
- Severity

---

# Business Rules

- Audit records cannot be edited.
- Audit records cannot be deleted.
- Every administrative action must be logged.
- Every approval workflow is logged.
- Sensitive data is masked where required.

---

# Validation Rules

ConstructPulse validates:

✓ Authenticated User

✓ Module

✓ Timestamp

✓ Company Scope

✓ Event Type

---

# Failure Scenarios

Examples include:

- Audit storage unavailable
- Corrupted event
- Duplicate event
- Invalid metadata
- Unauthorized access attempt

---

# Audit Events

The audit system itself records:

- Audit Viewed
- Audit Exported
- Audit Filter Applied

---

# Notifications

Security administrators receive alerts for:

- Multiple failed login attempts
- Suspicious administrator activity
- Permission escalation
- Mass data exports
- Unusual login locations

---

# Production Considerations

Supports:

- Unlimited audit history
- Multi-company isolation
- Immutable event storage
- Security monitoring
- Compliance investigations
- Historical reporting

---

# Future Enhancements

Future releases may include:

- SIEM integration
- Real-time threat detection
- AI anomaly detection
- Digital signatures
- Blockchain audit verification
- Security risk scoring

# 6.20 Business Continuity, Backup & Disaster Recovery Workflow

## Overview

The Business Continuity, Backup & Disaster Recovery Workflow ensures that ConstructPulse remains available, secure, and recoverable during unexpected failures.

Construction operations rely on accurate workforce visibility, attendance records, compliance information, and emergency management.

The platform is therefore designed with resilience in mind, minimizing operational disruption while protecting critical business data.

This workflow defines how ConstructPulse detects failures, protects data, restores services, and maintains operational continuity.

---

# Objectives

The workflow is designed to:

- Protect operational data
- Ensure high system availability
- Minimize downtime
- Recover from failures
- Maintain data integrity
- Support disaster recovery
- Enable business continuity

---

# Actors

Primary Actors

- System Administrator
- DevOps Engineer

Secondary Actors

- Company Administrator
- Director
- Operations Manager
- IT Support

---

# Failure Types

ConstructPulse prepares for multiple failure scenarios.

Examples include:

Infrastructure Failures

- Server Failure
- Database Failure
- Network Failure
- Storage Failure

Application Failures

- API Failure
- Authentication Failure
- Background Job Failure

Operational Failures

- Human Error
- Incorrect Configuration
- Accidental Deletion

External Events

- Internet Outage
- Cloud Provider Outage
- Power Failure
- Natural Disaster

---

# Backup Strategy

ConstructPulse performs:

- Automated Daily Database Backups
- Incremental Backups
- Weekly Full Backups
- Configuration Backups
- Document Storage Backups
- Audit Log Backups

Backups are encrypted before storage.

---

# Disaster Recovery Workflow

## Step 1 — Failure Detection

ConstructPulse continuously monitors:

- API Health
- Database Health
- Authentication Services
- Storage Availability
- Notification Services

Failures trigger automated alerts.

---

## Step 2 — Incident Classification

Failures are categorized as:

Low

Medium

High

Critical

Severity determines recovery procedures.

---

## Step 3 — Notification

Responsible personnel receive alerts.

Notifications include:

- Email
- Push Notification
- SMS (Future)

---

## Step 4 — Recovery

Recovery procedures include:

- Restart Services
- Restore Database
- Restore Configuration
- Restore Storage
- Reconnect Integrations

---

## Step 5 — Verification

ConstructPulse validates:

✓ Database Integrity

✓ Authentication

✓ Attendance Services

✓ Emergency Module

✓ QR Validation

✓ GPS Services

---

## Step 6 — Return to Service

Once verification succeeds:

Services resume.

Users are notified.

Incident timeline is archived.

---

# Offline Operation

If internet connectivity is unavailable:

Mobile applications continue to:

- Display worker profile
- Display safety documents
- Display emergency contacts
- Cache attendance requests
- Queue check-ins
- Queue check-outs

Queued operations synchronize automatically once connectivity is restored.

---

# Data Retention

ConstructPulse retains:

Attendance Records

7 Years

Incident Reports

Permanent

Emergency Reports

Permanent

Audit Logs

Permanent

Worker History

Employment Duration + Retention Policy

Backups

Configurable

Organizations may configure retention policies according to legal requirements.

---

# Recovery Objectives

Target Recovery Time Objective (RTO)

< 1 Hour

Target Recovery Point Objective (RPO)

< 15 Minutes

These objectives may vary depending on deployment architecture.

---

# Business Rules

- Backups cannot be manually modified.
- Recovery events are audited.
- Backup encryption is mandatory.
- Production recovery requires authorization.
- Disaster recovery tests should be performed regularly.

---

# Validation Rules

ConstructPulse validates:

✓ Backup Integrity

✓ Encryption

✓ Restore Success

✓ Database Consistency

✓ Authentication

---

# Failure Scenarios

Examples include:

- Backup corruption
- Failed restore
- Storage unavailable
- Authentication unavailable
- Notification delivery failure

---

# Audit Events

ConstructPulse records:

- Backup Started
- Backup Completed
- Restore Started
- Restore Completed
- Recovery Verified
- Disaster Recovery Test Completed

---

# Notifications

System Administrators receive:

- Backup Failure
- Recovery Started
- Recovery Completed
- Infrastructure Alerts
- Database Alerts

---

# Production Considerations

Supports:

- Cloud deployment
- Multi-region deployment
- Automatic backups
- Disaster recovery testing
- High availability
- Offline synchronization

---

# Future Enhancements

Future releases may include:

- Multi-region active-active deployment
- Automated failover
- Kubernetes self-healing
- Edge synchronization
- AI infrastructure monitoring
- Predictive failure detection


