import os
import sys
import uuid
import httpx
from datetime import datetime

API_URL = "http://localhost:8000"
DEMO_AUTH = "true" # By passing strictly 

import os
import sys
import uuid
from app.db.database import SessionLocal
from app.models.models import User, Site, UserRole, WorkerStatus, SiteQRCode
from fastapi.testclient import TestClient
from main import app
from app.core.security import create_access_token

def run():
    db = SessionLocal()
    client = TestClient(app)
    
    # Get the admin user
    admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()
    if not admin:
        print("No COMPANY_ADMIN found. Run verify_flow.py or bootstrap_admin.py first.")
        sys.exit(1)
        
    admin_token = create_access_token(admin.id)
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 4. Register a new worker (bypassing the endpoint to simulate a PENDING worker manually if DEMO_AUTH is on)
    new_phone = f"+1555{uuid.uuid4().hex[:7]}"
    new_worker = User(
        name="Test Worker Pending",
        phone_number=new_phone,
        role=UserRole.WORKER,
        firebase_uid=f"firebase_{new_phone}",
        status=WorkerStatus.PENDING,
        is_active=False
    )
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    print(f"Registered new worker: {new_worker.name} with ID: {new_worker.id}")
    
    # 5. Approve worker
    print("\n--- Approving Worker ---")
    response = client.put(f"/api/v1/users/{new_worker.id}/approve", headers=admin_headers)
    print(f"API Response: {response.json()}")
    
    db.refresh(new_worker)
    print(f"Worker status is now: {new_worker.status.value}, is_active: {new_worker.is_active}")
    
    # 6. Assign worker to site
    # Create or get a site
    site = db.query(Site).first()
    print(f"\n--- Assigning Worker to Site: {site.name} ---")
    assign_payload = {"worker_id": new_worker.id}
    response = client.post(f"/api/v1/sites/{site.id}/assign-worker", json=assign_payload, headers=admin_headers)
    print(f"API Response: {response.json()}")
    
    # 7. Verify worker can successfully scan QR and check in
    # Create a fresh QR code to avoid expiration
    from datetime import datetime, timedelta, timezone
    new_qr = SiteQRCode(
        site_id=site.id,
        qr_token=str(uuid.uuid4()),
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)
        
    worker_token = create_access_token(new_worker.id)
    worker_headers = {"Authorization": f"Bearer {worker_token}"}
    
    print("\n--- Worker QR Check-In ---")
    checkin_payload = {
        "site_id": site.id,
        "qr_token": new_qr.qr_token,
        "gps_latitude": site.latitude,
        "gps_longitude": site.longitude
    }
    response = client.post("/api/v1/attendance/check-in", json=checkin_payload, headers=worker_headers)
    print(f"API Response: {response.json()}")

if __name__ == "__main__":
    run()
