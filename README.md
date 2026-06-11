# ConstructPulse

## Overview
ConstructPulse is an enterprise-grade mobile application and backend service designed to manage construction workforce operations. It provides real-time visibility into site occupancy, automated attendance tracking via QR codes, safety compliance, and immediate emergency evacuation accountability. ConstructPulse scales across multiple construction sites, managing hundreds of contractors and workers efficiently.

## Features

### System Admin
- Global platform configuration and monitoring
- Multi-company onboarding and management
- Comprehensive platform analytics and usage tracking

### Company Admin
- **Workforce Management:** Approve, suspend, and manage all workers in the company
- **Site Management:** Create and configure construction sites, generate site-specific QR codes
- **Dashboard & Analytics:** Real-time visibility into site occupancy, checked-in workers, and live attendance metrics
- **Emergency Mustering:** Trigger site-wide emergency musters and track evacuation status
- **Company Setup:** Manage departments and contractors

### Worker
- **Attendance:** Scan site QR codes to check in and check out effortlessly
- **Dashboard:** View personal attendance history, active site status, and daily hours
- **Profile:** Manage emergency contacts and personal details
- **Emergency:** Mark oneself as safe during an active emergency muster

## Tech Stack

- **Frontend:** Flutter (Dart) mobile application
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (with SQLAlchemy ORM)
- **Authentication:** Firebase Auth (Phone/OTP) + JWT Bearer tokens
- **State Management:** Riverpod (Flutter)
- **Routing:** GoRouter (Flutter)

## Architecture

ConstructPulse employs a decoupled client-server architecture:
- The **Backend API** provides a RESTful interface using FastAPI, enforcing strict role-based access control (RBAC) and ensuring data isolation between companies. It uses SQLAlchemy for database operations and Alembic for schema migrations.
- The **Frontend Mobile App** follows a feature-first, domain-driven directory structure. It utilizes Riverpod for reactive state management and GoRouter for declarative navigation. The UI is built with a custom design system to ensure brand consistency and accessibility.

## Folder Structure

- `backend/`: FastAPI Python application
  - `app/api/`: REST endpoints and routers
  - `app/core/`: Configuration, security, and application settings
  - `app/db/`: Database session management
  - `app/models/`: SQLAlchemy database models
  - `app/schemas/`: Pydantic models for validation
  - `app/services/`: Core business logic
- `mobile/`: Flutter Dart application
  - `lib/core/`: App-wide utilities, routing, networking, and design system
  - `lib/features/`: Feature modules (e.g., auth, attendance, dashboard, sites, workforce)
- `docs/`: Project documentation and guides

## Setup Instructions

### Database Setup
1. Install PostgreSQL.
2. Create a database (e.g., `constructpulse`).
3. Set the `DATABASE_URL` in your `.env` file.

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd mobile
flutter pub get
flutter run
```

## Environment Variables

A `.env.example` file is provided in the `backend/` directory.

Required variables:
- `DATABASE_URL`: Connection string for PostgreSQL
- `SECRET_KEY`: Cryptographic key for session/security operations
- `ALGORITHM`: JWT algorithm (e.g., HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT expiration time
- `FIREBASE_PROJECT_ID`: Firebase project identifier

## API Overview

- `/auth`: Registration, login, and token generation
- `/users`: User profile management and directory
- `/sites`: Construction site management
- `/attendance`: Check-in, check-out, and live occupancy tracking
- `/dashboard`: Real-time analytics and Key Performance Indicators (KPIs)
- `/emergency`: Muster triggering and safety reporting

## Screenshots Section

*(Placeholders for future screenshots)*
- `[Login / Registration]`
- `[Admin Dashboard]`
- `[Worker Dashboard]`
- `[Site QR Scanner]`
- `[Emergency Muster Report]`
- `[Workforce Directory]`

## Future Enhancements

- Advanced Analytics Dashboard
- Automated Payroll Integration
- Geofenced Check-ins
- Offline Mode with Sync

## Contributors
- ConstructPulse Development Team
