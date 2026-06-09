import os
import sys
import requests
import time
from datetime import datetime, timezone

sys.path.append(os.path.abspath('.'))
from app.db.database import SessionLocal
from app.models.models import User, Site, SiteQRCode, Attendance

# 1. Login to get token
resp = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json={"token": "DEMO_TOKEN_+18790638289"})
token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

db = SessionLocal()
worker = db.query(User).filter(User.phone_number == '+18790638289').first()
site = worker.assigned_sites[0]
qr = db.query(SiteQRCode).filter(SiteQRCode.site_id == site.id).order_by(SiteQRCode.created_at.desc()).first()

# Fix existing check-ins to CHECKED_OUT
db.query(Attendance).filter(Attendance.user_id == worker.id, Attendance.status == "CHECKED_IN").update({"status": "CHECKED_OUT", "check_out_time": datetime.now(timezone.utc)})
db.commit()

print("--- INITIAL STATE ---")
att_before = db.query(Attendance).filter(Attendance.user_id == worker.id).all()
print(f"Total Attendances: {len(att_before)}")

print("\n--- CHECK-IN ---")
checkin_data = {
    "site_id": site.id,
    "qr_token": qr.qr_token,
    "gps_latitude": site.latitude,
    "gps_longitude": site.longitude
}
resp = requests.post("http://127.0.0.1:8000/api/v1/attendance/check-in", json=checkin_data, headers=headers)
print("Check-in Response:", resp.status_code, resp.json())

time.sleep(1)

print("\n--- CHECK-OUT ---")
checkout_data = {
    "site_id": site.id,
    "qr_token": qr.qr_token,
    "gps_latitude": site.latitude,
    "gps_longitude": site.longitude
}
resp = requests.post("http://127.0.0.1:8000/api/v1/attendance/check-out", json=checkout_data, headers=headers)
print("Check-out Response:", resp.status_code, resp.json())

print("\n--- FINAL STATE ---")
att_after = db.query(Attendance).filter(Attendance.user_id == worker.id).order_by(Attendance.check_in_time.desc()).first()
print(f"Latest Attendance Record ID: {att_after.id}")
print(f"Check In Time: {att_after.check_in_time}")
print(f"Check Out Time: {att_after.check_out_time}")
print(f"Status: {att_after.status}")
