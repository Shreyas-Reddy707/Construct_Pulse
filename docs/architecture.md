# System Architecture

ConstructPulse employs a modern, decoupled client-server architecture, enabling high scalability, independent deployments, and secure data handling.

## High-Level Diagram
1. **Mobile Application (Frontend):** Flutter, Dart
2. **REST API (Backend):** FastAPI, Python
3. **Database Layer:** PostgreSQL, SQLAlchemy
4. **Identity Provider:** Firebase Auth

## Frontend Architecture (Mobile)
The mobile application is built using Flutter and follows a **Feature-First Domain-Driven Design**.

### Core Technologies
- **State Management:** Riverpod for reactive state caching and dependency injection.
- **Routing:** GoRouter for declarative, path-based navigation with route guards.
- **Networking:** Dio with custom interceptors for JWT injection and error handling.
- **UI:** A custom token-based design system ensuring consistency across dark/light modes.

### Directory Structure (`mobile/lib`)
- `core/`: Constants, network clients, routers, global state, and theme data.
- `features/`: Isolated domain modules (e.g., `auth`, `attendance`, `dashboard`). Each feature typically contains:
  - `data/`: Repositories and models.
  - `domain/`: Business entities and use cases.
  - `presentation/`: Screens, widgets, and Riverpod providers.

## Backend Architecture (API)
The backend is built with FastAPI, utilizing asynchronous path operations and Dependency Injection.

### Core Technologies
- **Framework:** FastAPI (Python 3.10+)
- **ORM:** SQLAlchemy for database interaction
- **Migrations:** Alembic for schema versioning
- **Authentication:** Firebase Admin SDK for JWT verification

### Directory Structure (`backend/app`)
- `api/`: Route definitions and dependency injections (e.g., `deps.py`).
- `core/`: Environment settings (`config.py`) and security configurations.
- `db/`: Database connection engines and base declarative models.
- `models/`: SQLAlchemy database models representing tables.
- `schemas/`: Pydantic models for request validation and response serialization.
- `services/`: Core business logic, keeping routers lean.

## Security & Authentication
1. User authenticates via Firebase OTP (SMS).
2. Mobile app retrieves the Firebase JWT and sends it to the backend (`/api/v1/auth/login`).
3. Backend verifies the Firebase JWT.
4. Backend issues a custom access token (JWT) containing user identity and role.
5. All protected endpoints validate the access token and enforce strict Role-Based Access Control (RBAC).

## Data Isolation
ConstructPulse is a multi-tenant platform. Data isolation is achieved by associating almost all entities (Sites, Workers, Attendances) with a `company_id`. The backend `get_current_user` dependency automatically scopes database queries to the user's `company_id`, preventing cross-company data leakage.
