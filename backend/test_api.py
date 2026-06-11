from fastapi.testclient import TestClient
from main import app
from app.db.database import SessionLocal
from app.models.models import User

db = SessionLocal()
# get an admin token
admin = db.query(User).filter(User.role == 'COMPANY_ADMIN').first()
db.close()

client = TestClient(app)
response = client.post("/api/v1/auth/login", data={"username": admin.phone, "password": "password"})
token = response.json()["access_token"]

resp = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {token}"})
for u in resp.json():
    print(u["id"], u["status"], u["role"])
