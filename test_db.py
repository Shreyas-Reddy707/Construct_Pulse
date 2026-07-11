import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app.db.database import SessionLocal
from app.models.models import Company, User, Site, Contractor, Department, RegistrationRequest

db = SessionLocal()
try:
    print(f'Companies: {db.query(Company).count()}')
    users = db.query(User).all()
    print(f'Users: {len(users)}')
    for u in users:
        print(f"  - {u.name} | {u.phone_number} | {u.role.value} | {u.status.value}")
    print(f'Sites: {db.query(Site).count()}')
    print(f'Contractors: {db.query(Contractor).count()}')
    print(f'Departments: {db.query(Department).count()}')
    print(f'Registration Requests: {db.query(RegistrationRequest).count()}')
except Exception as e:
    print("Database error:", e)
