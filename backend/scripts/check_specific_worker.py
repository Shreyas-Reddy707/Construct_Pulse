import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
from app.db.database import SessionLocal
from app.models.models import User, UserRole
from app.core.security import create_access_token

db = SessionLocal()
admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()
if not admin:
    print("No admin found")
    sys.exit(1)

client = TestClient(app)
token = create_access_token(admin.id)
res = client.get(f'/api/v1/users/ae398ec8-b093-4506-8a1c-b97572855ce7', headers={'Authorization': f'Bearer {token}'})
import json
print(json.dumps(res.json(), indent=2))
