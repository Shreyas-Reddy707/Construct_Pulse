# ConstructPulse

**Workforce Intelligence Platform**

ConstructPulse is an enterprise-grade mobile application and backend service designed to modernize and simplify construction workforce management. It provides end-to-end solutions for attendance tracking, emergency mustering, safety compliance, site access, and overall workforce visibility.

---

## 🌟 Key Features

*   **Role-Based Access Control & Dashboards:** Tailored experiences for Company Admins, Site Managers, and General Workers.
*   **Authentication & Onboarding:** Secure Firebase phone authentication with OTP, paired with a robust registration workflow requiring Company Admin approval for new workers.
*   **Real-time Attendance Tracking:** Workers check in and out of sites using printable QR codes.
*   **Site Management:** Create and manage construction sites, assign workers, and generate site-specific QR codes.
*   **Workforce Directory:** Complete visibility into the company's workforce, including nested departments, contractors, and individual worker profiles.
*   **Live Occupancy Monitoring:** Dashboards showing real-time metrics on site occupancy, department breakdowns, and contractor presence.
*   **Emergency Mustering:** Immediate emergency evacuation accountability tools to ensure worker safety during incidents.
*   **Additional Modules:** Foundations for Tasks, Planning, Payroll, Reports, and Notifications.

---

## 🏗️ Architecture Stack

### Frontend (Mobile App)
*   **Framework:** Flutter (Dart)
*   **State Management:** Riverpod
*   **Routing:** GoRouter
*   **Networking:** Dio
*   **Architecture Pattern:** Feature-first modular architecture

### Backend (REST API)
*   **Framework:** FastAPI (Python)
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Authentication:** Firebase Auth & JWT Bearer Tokens
*   **Database Migrations:** Alembic

---

## 🚀 Setup Instructions

### 1. PostgreSQL Database Setup
1. Ensure PostgreSQL is installed and running on your machine.
2. Create a new database named `constructpulse` (or your preferred name).

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   * **Windows:**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables. Copy `.env.example` to `.env` and configure your database URL:
   ```env
   DATABASE_URL=postgresql://postgres:YourPassword@localhost:5432/constructpulse
   SECRET_KEY=your_super_secret_jwt_key
   DEMO_AUTH=true
   ```
5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
6. (Optional) Seed the database with demo data:
   ```bash
   python scripts/seed_test_data.py
   ```
7. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be available at `http://localhost:8000`*

### 3. Frontend Setup
1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```
2. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app:
   ```bash
   flutter run
   ```
   *(We recommend running on an iOS Simulator, Android Emulator, or Chrome for web debugging)*

---

## 🔐 Authentication Modes

ConstructPulse supports two authentication modes, configurable via the frontend and backend:

1.  **Production Mode (Firebase):** Uses real SMS OTP verification via Firebase.
2.  **Demo Mode:** Allows bypassing actual SMS costs and Firebase limits during local development. 
    *   To enable on the backend, ensure `DEMO_AUTH=true` is set in your `.env`.
    *   To enable on the frontend, ensure `AppConstants.demoAuth = true` is set in `mobile/lib/core/constants/app_constants.dart`.
    *   In Demo mode, you can log in using any registered phone number by entering the development OTP prefix.

---

## 🗺️ Future Roadmap

*   Advanced Analytics and Reporting Dashboards
*   Automated Payroll Integrations
*   Geofenced Auto Check-ins
*   Offline Mode with Background Sync
*   Equipment & Asset Tracking

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
