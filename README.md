# ConstructPulse

**Workforce Intelligence Platform**

ConstructPulse is an enterprise-grade mobile application and backend service designed to manage construction workforce attendance, emergency mustering, safety compliance, and site access.

## Project Overview

This system provides real-time visibility into site occupancy, automated attendance tracking via QR codes, and immediate emergency evacuation accountability. It is designed to scale across multiple construction sites, managing hundreds of contractors and workers.

## Architecture


- **Frontend:** Flutter (Dart) mobile application
  - State Management: Riverpod
  - Routing: GoRouter
  - Network: Dio
- **Backend:** FastAPI (Python)
  - Database: PostgreSQL via SQLAlchemy ORM
  - Authentication: Firebase Auth + JWT Bearer
  - Migrations: Alembic

## Screenshots
*(Placeholders for future screenshots)*
- `[Login Screen]`
- `[Worker Dashboard]`
- `[Manager Dashboard]`
- `[QR Code Scanner]`
- `[Emergency Muster Report]`

## Setup Instructions

### Environment Variables
A `.env.example` file is provided in the `backend` directory. Do not commit actual `.env` files to version control.
```
DATABASE_URL=postgresql://user:password@host/db
SECRET_KEY=your_secret_here
JWT_SECRET=your_jwt_secret_here
```


### PostgreSQL Setup
1. Install PostgreSQL.
2. Create a database named `constructpulse` (or as defined in your `.env`).
3. Set the `DATABASE_URL` in your `.env`.

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

## Running Locally

To run the full stack locally for development:
1. Start the PostgreSQL database.
2. Start the FastAPI backend on port 8000.
3. Launch the Flutter app via `flutter run`.

*Note: A demo authentication mode is available in the Flutter app for testing without Firebase SMS billing. Set `AppConstants.demoAuth = true` to enable it (default is false for production).*

## Future Roadmap

- Advanced Analytics Dashboard
- Automated Payroll Integration
- Geofenced Check-ins
- Offline Mode with Sync

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
