import os
import sys
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
from app.db.database import SessionLocal, engine
from app.models.models import User, UserRole
from app.core.security import create_access_token
from sqlalchemy import text

db = SessionLocal()

# 1. Direct Database Query
worker_id = '16daccd6-7f2d-4152-ba81-dbefb4f0f49b'
query = text("""
    SELECT
        id,
        user_id,
        check_in_time,
        check_out_time,
        status
    FROM attendances
    WHERE user_id = :worker_id
    ORDER BY check_in_time DESC;
""")

result = db.execute(query, {'worker_id': worker_id}).fetchall()
print("\n--- RAW DATABASE QUERY RESULTS ---")
for r in result:
    print(dict(r._mapping))

# 2. Get Admin Token
admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()
if not admin:
    print("No admin found")
    sys.exit(1)

client = TestClient(app)
token = create_access_token(admin.id)
headers = {'Authorization': f'Bearer {token}'}

# 3. History API Response
print("\n--- ATTENDANCE HISTORY API RESULTS ---")
res_history = client.get(f'/api/v1/attendance/history/{worker_id}', headers=headers)
print(f"Status Code: {res_history.status_code}")
print(json.dumps(res_history.json(), indent=2))

# 4. Live Attendance API Response
print("\n--- LIVE ATTENDANCE API RESULTS ---")
res_live = client.get('/api/v1/attendance/live', headers=headers)
print(f"Status Code: {res_live.status_code}")
print(json.dumps(res_live.json(), indent=2))
