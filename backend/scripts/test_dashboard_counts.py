import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
from app.db.database import SessionLocal
from app.models.models import User, UserRole, WorkerStatus
from app.core.security import create_access_token

db = SessionLocal()
admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()
worker = db.query(User).filter(User.company_id == admin.company_id, User.role == UserRole.WORKER).first()

client = TestClient(app)
token = create_access_token(admin.id)

print("--- BEFORE SUSPENSION ---")
res_dashboard_before = client.get('/api/v1/dashboard/summary', headers={'Authorization': f'Bearer {token}'})
print("Dashboard:", json.dumps(res_dashboard_before.json(), indent=2))

print("\n--- SUSPENDING WORKER ---")
res_suspend = client.put(f'/api/v1/users/{worker.id}/suspend', headers={'Authorization': f'Bearer {token}'})
print("Suspend Status:", res_suspend.status_code)

print("\n--- AFTER SUSPENSION ---")
res_dashboard_after = client.get('/api/v1/dashboard/summary', headers={'Authorization': f'Bearer {token}'})
print("Dashboard:", json.dumps(res_dashboard_after.json(), indent=2))

# Revert
client.put(f'/api/v1/users/{worker.id}/reactivate', headers={'Authorization': f'Bearer {token}'})
