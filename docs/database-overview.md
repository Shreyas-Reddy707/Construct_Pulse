# Database Overview

ConstructPulse uses PostgreSQL as its primary relational database. The schema is managed using SQLAlchemy ORM and Alembic migrations.

## Core Entities

### 1. Company (`companies`)
The top-level entity representing a construction firm or organization.
- **Fields:** `id`, `company_name`, `registration_number`, `contact_email`, `contact_phone`
- **Relationships:** One-to-Many with Users, Sites, Departments, and Contractors.

### 2. User (`users`)
Represents all personnel in the system, ranging from field workers to system administrators.
- **Fields:** `id`, `firebase_uid`, `phone_number`, `name`, `role`, `company_id`, `status`, `is_active`
- **Roles:** `Worker`, `Supervisor`, `Contractor`, `Company Admin`, `System Admin`
- **Status:** `pending`, `approved`, `rejected`, `suspended`

### 3. Site (`sites`)
Physical construction locations where workers check in.
- **Fields:** `id`, `company_id`, `name`, `address`, `latitude`, `longitude`, `qr_code_hash`, `status`
- **Relationships:** Many-to-Many with Departments, Contractors, and Users (assigned workers).

### 4. Attendance (`attendances`)
Records of a worker checking in and out of a site.
- **Fields:** `id`, `worker_id`, `site_id`, `company_id`, `check_in_time`, `check_out_time`, `status`, `notes`
- **Logic:** Live occupancy is calculated by selecting records where `check_out_time` is NULL and `status` is `CHECKED_IN`.

### 5. Emergency Muster (`emergency_musters` & `muster_responses`)
Used during site evacuations to track worker safety.
- **Muster:** `site_id`, `company_id`, `triggered_by`, `status` (active/resolved)
- **Response:** `muster_id`, `worker_id`, `status` (safe/unaccounted), `reported_at`

## Schema Migrations

All schema changes are tracked via Alembic.
To apply migrations locally:
```bash
cd backend
alembic upgrade head
```

To create a new migration after modifying `models.py`:
```bash
alembic revision --autogenerate -m "Add new column"
```
