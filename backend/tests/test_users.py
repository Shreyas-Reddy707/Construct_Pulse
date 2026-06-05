import pytest
from fastapi.testclient import TestClient
from main import app
from app.models.models import User, UserRole, WorkerStatus

def test_user_filtering_by_status(client, db_session, setup_data):
    from app.core.security import create_access_token
    # Set the original user to ADMIN so we have permission
    admin_user = db_session.query(User).filter(User.id == setup_data["user_id"]).first()
    admin_user.role = UserRole.COMPANY_ADMIN
    admin_user.status = WorkerStatus.APPROVED
    db_session.commit()
    
    headers = {"Authorization": f"Bearer {setup_data['token']}"}

    import uuid
    uid = str(uuid.uuid4())[:8]
    # Create test users with different statuses
    user1 = User(name="User 1", phone_number=f"+1{uid}", role=UserRole.WORKER, status=WorkerStatus.APPROVED, company_id=admin_user.company_id)
    user2 = User(name="User 2", phone_number=f"+2{uid}", role=UserRole.WORKER, status=WorkerStatus.PENDING, company_id=admin_user.company_id)
    user3 = User(name="User 3", phone_number=f"+3{uid}", role=UserRole.WORKER, status=WorkerStatus.SUSPENDED, company_id=admin_user.company_id)
    db_session.add_all([user1, user2, user3])
    db_session.commit()

    # Test approved
    response = client.get("/api/v1/users?status=approved", headers=headers)
    assert response.status_code == 200
    assert any(u["phone_number"] == f"+1{uid}" for u in response.json())
    assert not any(u["phone_number"] == f"+2{uid}" for u in response.json())
    assert not any(u["phone_number"] == f"+3{uid}" for u in response.json())

    # Test pending
    response = client.get("/api/v1/users?status=pending", headers=headers)
    assert response.status_code == 200
    assert any(u["phone_number"] == f"+2{uid}" for u in response.json())

    # Test suspended
    response = client.get("/api/v1/users?status=suspended", headers=headers)
    assert response.status_code == 200
    assert any(u["phone_number"] == f"+3{uid}" for u in response.json())

def test_prevent_self_suspension(client, db_session, setup_data):
    headers = {"Authorization": f"Bearer {setup_data['token']}"}
    response = client.put(f"/api/v1/users/{setup_data['user_id']}/suspend", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot suspend yourself"

def test_prevent_admin_suspension(client, db_session, setup_data):
    admin_user = db_session.query(User).filter(User.id == setup_data["user_id"]).first()
    headers = {"Authorization": f"Bearer {setup_data['token']}"}

    import uuid
    uid = str(uuid.uuid4())[:8]
    another_admin = User(phone_number=f"+9{uid}", role=UserRole.COMPANY_ADMIN, status=WorkerStatus.APPROVED, company_id=admin_user.company_id)
    db_session.add(another_admin)
    db_session.commit()

    response = client.put(f"/api/v1/users/{another_admin.id}/suspend", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Admin users cannot be suspended"
