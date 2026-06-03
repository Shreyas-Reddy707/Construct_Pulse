from fastapi.testclient import TestClient
import json
from sqlalchemy.orm import Session
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.main import app
from app.db.database import SessionLocal
from app.models.models import User, Site, SiteQRCode, Attendance, UserRole, WorkerStatus, AttendanceStatus
from app.core.config import settings

client = TestClient(app)
db = SessionLocal()

# 1. Setup a test COMPANY_ADMIN user and a Site
user = db.query(User).filter(User.phone_number == "+19999999999").first()
if not user:
    user = User(
        phone_number="+19999999999",
        name="Admin Tester",
        role=UserRole.COMPANY_ADMIN,
        status=WorkerStatus.APPROVED,
        is_active=True,
        firebase_uid="test-firebase-uid"
    )
    db.add(user)
    db.commit()

site = db.query(Site).filter(Site.name == "Demo Metro Tower").first()
if not site:
    site = Site(
        name="Demo Metro Tower",
        address="123 Test St",
        latitude=10.0,
        longitude=10.0,
        geofence_radius_meters=100.0,
        status="active",
        company_id="dummy-company"
    )
    db.add(site)
    db.commit()

db.refresh(user)
db.refresh(site)

# Login to get token (using a backdoor or mock if firebase is disabled)
# Since we use DEMO_AUTH or Firebase, wait... the endpoint /auth/login uses Firebase.
# Let's just create a token directly if we can't login, or use dependency override.
from app.api.deps import get_current_user
app.dependency_overrides[get_current_user] = lambda: user

# Verify 1 & 2: Code paths already analyzed.

# Verify 3: Login Stability
# N/A for backend test client.

# Verify 4: QR Check-In
print("\n--- Verify 4: QR Check-In ---")
# Generate QR
qr_resp = client.post(f"/api/v1/sites/{site.id}/generate-qr")
qr_data = qr_resp.json()
qr_token = qr_data['qr_token']

checkin_payload = {
    "site_id": site.id,
    "qr_token": qr_token,
    "gps_latitude": 10.0,
    "gps_longitude": 10.0
}
print(f"Request Payload: {json.dumps(checkin_payload, indent=2)}")

checkin_resp = client.post("/api/v1/attendance/check-in", json=checkin_payload)
print(f"API Response: {json.dumps(checkin_resp.json(), indent=2)}")

# Verify DB Row
att = db.query(Attendance).filter(Attendance.user_id == user.id, Attendance.site_id == site.id, Attendance.status == AttendanceStatus.CHECKED_IN).first()
print(f"Database Row: id={att.id}, user_id={att.user_id}, site_id={att.site_id}, status={att.status.name}, check_in_time={att.check_in_time}")

# Verify 5: QR Check-Out
print("\n--- Verify 5: QR Check-Out ---")
checkout_payload = {
    "site_id": site.id,
    "qr_token": qr_token,
    "gps_latitude": 10.0,
    "gps_longitude": 10.0
}
print(f"Request Payload: {json.dumps(checkout_payload, indent=2)}")

checkout_resp = client.post("/api/v1/attendance/check-out", json=checkout_payload)
print(f"API Response: {json.dumps(checkout_resp.json(), indent=2)}")

# Verify DB Row
db.refresh(att)
print(f"Database Row: id={att.id}, status={att.status.name}, check_in_time={att.check_in_time}, check_out_time={att.check_out_time}")

