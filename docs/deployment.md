# Deployment Guide

This guide covers deploying the ConstructPulse backend to a production environment.

## 1. Infrastructure Requirements
- **Database:** Managed PostgreSQL (e.g., AWS RDS, Heroku Postgres, or Supabase).
- **Application Server:** A platform capable of running Docker containers or native Python (e.g., AWS ECS, Render, Railway, or Heroku).
- **Identity:** A Firebase Project configured with Phone Authentication.

## 2. Environment Variables
Ensure the production environment contains the following securely stored secrets:

```env
# Database configuration
DATABASE_URL=postgresql://production_user:secure_password@production_host:5432/constructpulse

# Security keys
SECRET_KEY=your_highly_secure_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
# Additionally, the FIREBASE_APPLICATION_CREDENTIALS path or JSON representation is required
# if not running on Google Cloud infrastructure.
```

## 3. Docker Deployment (Recommended)
A `docker-compose.yml` file is provided in the `backend/` directory for containerized deployment.

1. Build the Docker image:
   ```bash
   docker build -t constructpulse-api .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env constructpulse-api
   ```

## 4. Database Migrations
Before routing traffic to the API, apply pending migrations to the production database:
```bash
# Executed from within the container or deployment pipeline
alembic upgrade head
```

## 5. Security Checklist
- Disable `demoAuth` in the Flutter mobile application before compiling the production `apk`/`ipa`.
- Ensure all API traffic is served over HTTPS.
- Configure CORS origins in FastAPI to only allow traffic from expected clients if deploying a web dashboard.
- Verify that Firebase App Check is enabled to prevent unauthorized API requests to Firebase.
