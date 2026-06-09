import os
import sys
import requests
import time
from datetime import datetime

sys.path.append(os.path.abspath('.'))
from app.db.database import SessionLocal
from app.models.models import User, UserRole

db = SessionLocal()
admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()
print(f"Admin phone: {admin.phone_number}")

# Login
resp = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json={"token": f"DEMO_TOKEN_{admin.phone_number}"})
token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

site_id = "65a4d83f-1343-4652-a249-17b926f1b386"
print("\n--- GENERATE QR ---")
resp = requests.post(f"http://127.0.0.1:8000/api/v1/sites/{site_id}/generate-qr", headers=headers)
print("Status:", resp.status_code)
print("Response:", resp.json())

print("\n--- GET QR ---")
resp = requests.get(f"http://127.0.0.1:8000/api/v1/sites/{site_id}/qr", headers=headers)
print("Status:", resp.status_code)
print("Response:", resp.json())
