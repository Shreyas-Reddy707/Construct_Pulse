from fastapi.testclient import TestClient
from main import app
from app.db.database import SessionLocal
from app.models.models import User, UserRole
from app.api.deps import get_current_user

# create a mock user
db = SessionLocal()
admin = db.query(User).filter(User.role == UserRole.COMPANY_ADMIN).first()

def override_get_current_user():
    return admin

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)
response = client.get("/api/v1/users?status=pending")
print("Response status no slash:", response.status_code)

response2 = client.get("/api/v1/users/?status=pending")
print("Response status with slash:", response2.status_code)
