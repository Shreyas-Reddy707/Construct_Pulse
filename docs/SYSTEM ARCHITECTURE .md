# SYSTEM_ARCHITECTURE.md

> **Project:** ConstructPulse  
> **Version:** 2.0  
> **Document Type:** Enterprise System Architecture  
> **Status:** Production Design  
> **Prepared By:** Engineering Team  
> **Last Updated:** July 2026

---

# ConstructPulse Enterprise System Architecture

## 1. Introduction

ConstructPulse is a cloud-native **Construction Workforce Operating System (CWOS)** designed for construction companies to manage workforce operations, compliance, attendance, safety, emergency response, subcontractor coordination, communications, and analytics through a single integrated platform.

This document defines the complete technical architecture of the platform, including software architecture, infrastructure, security, scalability, integrations, and deployment strategy.

---

# 2. Architecture Goals

The architecture is designed around the following goals:

- Scalability
- High Availability
- Maintainability
- Security
- Performance
- Offline Capability
- Modular Design
- Cloud Native Deployment
- API First Development
- Enterprise Readiness

---

# 3. Architecture Principles

The following engineering principles guide the platform architecture.

## SOLID Principles

The application follows all SOLID principles to improve maintainability and extensibility.

## Separation of Concerns

Business logic, presentation, data access, and infrastructure remain isolated.

## Repository Pattern

Database access is abstracted through repositories.

## Dependency Injection

Dependencies are injected to improve testing and maintainability.

## Modular Architecture

Every business module remains independent while communicating through defined interfaces.

## Security by Design

Authentication, authorization, encryption, and auditing are implemented across every layer.

## Configuration over Hardcoding

Business rules are configurable through administration modules.

---

# 4. High-Level Architecture

```
                 Mobile App (Flutter)
                         │
                         ▼
                  REST API (HTTPS)
                         │
                         ▼
                FastAPI Backend Server
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Authentication     Business Logic     Background Jobs
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  PostgreSQL Database
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Firebase Auth     Notification APIs    File Storage
```

---

# 5. Technology Stack

## Frontend

- Flutter
- Dart
- Riverpod
- GoRouter
- Dio
- Material 3

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn

---

## Database

- PostgreSQL

---

## Authentication

- Firebase Phone Authentication
- JWT Access Tokens
- Refresh Tokens

---

## DevOps

- Docker
- Docker Compose
- GitHub
- GitHub Actions
- Ubuntu Server
- Nginx

---

## Future Technologies

- Redis
- Celery
- Prometheus
- Grafana
- Sentry
- Kubernetes

---

# 6. Repository Structure

```
ConstructPulse/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── core/
│   │
│   ├── alembic/
│   └── tests/
│
├── mobile/
│   ├── lib/
│   │   ├── features/
│   │   ├── core/
│   │   ├── shared/
│   │   ├── widgets/
│   │   └── services/
│   │
│   └── test/
│
├── docs/
├── scripts/
└── deployment/
```

---

# 7. Domain Modules

The platform is divided into independent business modules.

- Authentication
- Company Management
- Projects
- Sites
- Workforce
- Departments
- Trades
- Subcontractors
- Attendance
- GPS Validation
- QR Validation
- Compliance
- Certifications
- Safety
- Emergency Muster
- Visitors
- Vehicles
- Communications
- Toolbox Talks
- Incident Management
- Asset Management
- Analytics
- Reports
- Notifications
- Administration
- Audit Logs

---

# 8. Database Architecture

Primary database:

- PostgreSQL

Primary design principles:

- UUID Primary Keys
- Foreign Key Constraints
- Database Indexing
- Soft Delete
- Transaction Support
- Audit Fields
- Migration Management using Alembic

---

# 9. Core Entity Relationships

```
Company
│
├── Projects
│
├── Sites
│     │
│     ├── Site Managers
│     ├── Workers
│     ├── Visitors
│     ├── Assets
│     ├── Attendance
│     └── Emergencies
│
├── Departments
│
├── Trades
│
└── Subcontractors
      │
      └── Workers
```

---

# 10. Authentication Architecture

Authentication Flow

```
Phone Number

↓

Firebase OTP

↓

Firebase Verification

↓

Backend Verification

↓

JWT Token

↓

Secure Storage

↓

Authenticated API Requests
```

---

# 11. Authorization Architecture

Role-Based Access Control (RBAC)

```
Platform Owner

↓

Director

↓

Operations Manager

↓

Company Administrator

↓

Site Manager

↓

Safety Officer

↓

Supervisor

↓

Worker

↓

Visitor
```

Permissions are enforced at API level and UI level.

---

# 12. API Architecture

The backend exposes RESTful APIs.

Examples:

```
/auth
/users
/sites
/projects
/attendance
/emergency
/incidents
/assets
/visitors
/reports
/analytics
```

Features:

- Versioned APIs
- Standard HTTP Methods
- JWT Authentication
- Pagination
- Filtering
- Sorting
- Validation
- Consistent Error Responses

---

# 13. Backend Layer Architecture

```
API Layer

↓

Service Layer

↓

Repository Layer

↓

Database Layer
```

Responsibilities:

API Layer

- Validation
- Authentication
- Request Handling

Service Layer

- Business Logic
- Workflow Execution

Repository Layer

- Database Access

Database Layer

- PostgreSQL

---

# 14. Frontend Architecture

```
Presentation Layer

↓

Riverpod Providers

↓

Repositories

↓

API Client

↓

Backend
```

The Flutter application follows Feature-First Architecture.

---

# 15. Attendance Engine

Attendance validation follows multiple verification steps.

```
Worker

↓

GPS Check

↓

QR Scan

↓

Site Validation

↓

Compliance Check

↓

Attendance Recorded

↓

Occupancy Updated
```

Attendance is rejected if:

- GPS outside radius
- Invalid QR
- Expired QR
- Worker inactive
- Worker not assigned
- Compliance expired

---

# 16. Compliance Engine

```
Worker

↓

Certifications

↓

Site Requirements

↓

Compliance Validation

↓

Approved for Work
```

Compliance is evaluated before attendance.

---

# 17. Emergency Engine

```
Emergency Triggered

↓

Broadcast Notification

↓

Worker Muster

↓

Live Occupancy Tracking

↓

Final Muster Report
```

---

# 18. Notification Architecture

Notifications support:

- Push Notifications
- In-App Notifications

Future:

- SMS
- Email
- Microsoft Teams
- Slack

---

# 19. Background Jobs

Scheduled background processes include:

- Certificate Expiry Checks
- Daily Reports
- Attendance Cleanup
- Occupancy Snapshots
- Notification Scheduling
- Backup Verification
- Analytics Aggregation

---

# 20. Security Architecture

Security features include:

- HTTPS
- JWT Authentication
- Refresh Tokens
- Firebase OTP
- Secure Storage
- GPS Validation
- QR Validation
- RBAC
- Audit Logging
- Input Validation
- SQL Injection Protection
- Rate Limiting
- Secure Headers
- CORS Configuration

---

# 21. Logging Strategy

The platform maintains:

- Application Logs
- API Logs
- Security Logs
- Audit Logs
- Error Logs
- Infrastructure Logs

Logs are retained according to configurable retention policies.

---

# 22. Monitoring Strategy

Production monitoring includes:

- API Health
- Database Health
- Worker Attendance Rate
- GPS Validation Success
- QR Validation Success
- System Performance
- Error Rate
- Resource Utilization

Future monitoring tools:

- Prometheus
- Grafana
- OpenTelemetry
- Sentry

---

# 23. Deployment Architecture

```
Internet

↓

Nginx Reverse Proxy

↓

FastAPI Application

↓

Background Workers

↓

PostgreSQL Database

↓

Persistent Storage
```

Future deployments may include Kubernetes and cloud-native infrastructure.

---

# 24. CI/CD Pipeline

```
Developer

↓

GitHub

↓

Automated Tests

↓

Build

↓

Docker Image

↓

Deployment

↓

Production
```

---

# 25. Scalability Strategy

ConstructPulse supports growth through:

- Horizontal API Scaling
- Database Optimization
- Background Job Processing
- Modular Services
- Stateless Backend Design
- Future Redis Caching

Target growth:

- 1 Company
- 10 Companies
- 100 Companies
- 1000+ Companies

---

# 26. Future Microservice Evolution

Current Architecture

```
Modular Monolith
```

Future Architecture

```
Authentication Service

Attendance Service

Notification Service

Compliance Service

Emergency Service

Analytics Service

Asset Service
```

Services can be extracted independently as the platform scales.

---

# 27. Technical Risks

Potential risks include:

- GPS Spoofing
- QR Sharing
- Device Loss
- Offline Synchronization Conflicts
- Database Failures
- Authentication Service Outages
- Network Latency
- High Concurrent Attendance Loads

Mitigation strategies are documented for each identified risk.

---

# 28. Architecture Decision Records (ADR)

Major architectural decisions include:

- Flutter selected for cross-platform mobile development.
- FastAPI selected for high-performance backend APIs.
- PostgreSQL selected for relational data consistency.
- UUIDs selected for globally unique identifiers.
- Firebase Phone Authentication selected for secure OTP verification.
- Role-Based Access Control implemented for enterprise security.
- Modular Monolith adopted initially to simplify development while allowing future microservice extraction.

---

# 29. Domain Model

The platform is organized into bounded business domains.

```
Authentication
        │
        ▼
Identity & Access
        │
────────┼────────
│       │       │
▼       ▼       ▼
Workforce  Sites  Companies
│       │       │
├───────┼───────┤
▼       ▼       ▼
Attendance  Compliance  Assets
│       │       │
├───────┼───────┤
▼       ▼       ▼
Emergency  Incidents  Communications
        │
        ▼
Analytics & Reporting
        │
        ▼
Administration & Audit
```

Each domain is independently maintainable while participating in the overall platform architecture.

---

# 30. Conclusion

ConstructPulse has been architected as a scalable, secure, and modular Construction Workforce Operating System (CWOS) capable of supporting organizations from small contractors to enterprise construction companies.

The architecture emphasizes safety, compliance, operational visibility, and maintainability while providing a strong foundation for future AI capabilities, enterprise integrations, and international expansion.

By following this architecture, ConstructPulse can evolve from a workforce management platform into a comprehensive construction operations ecosystem that supports digital transformation across the construction industry.

---
**End of Document**
