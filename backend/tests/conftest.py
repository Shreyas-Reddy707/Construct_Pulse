import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from main import app
from app.models.models import User, Site, Attendance, SiteQRCode, AttendanceStatus, Company
from app.core.security import create_access_token
import uuid
from datetime import datetime, timezone, timedelta

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def setup_data():
    db_session = TestingSessionLocal()
    unique_suffix = str(uuid.uuid4())[:8]
    company = Company(company_name=f"Test Company {unique_suffix}")
    db_session.add(company)
    db_session.commit()
    
    from app.models.models import WorkerStatus
    user = User(firebase_uid=f"test_uid_{unique_suffix}", phone_number=f"+1000{unique_suffix}", name="Test User", company_id=company.id, status=WorkerStatus.APPROVED)
    db_session.add(user)
    db_session.commit()

    site = Site(name=f"Test Site {unique_suffix}", latitude=10.0, longitude=10.0, geofence_radius_meters=500.0, company_id=company.id)
    site.assigned_workers.append(user)
    db_session.add(site)
    db_session.commit()
    
    qr = SiteQRCode(site_id=site.id, qr_token=f"test_qr_token_{unique_suffix}", expires_at=datetime.now(timezone.utc) + timedelta(days=1))
    db_session.add(qr)
    db_session.commit()
    
    token = create_access_token(user.id)
    data = {
        "user_id": user.id, 
        "site_id": site.id, 
        "qr_token": qr.qr_token, 
        "token": token,
        "firebase_uid": user.firebase_uid
    }
    db_session.close()
    return data
