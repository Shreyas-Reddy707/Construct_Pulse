import os
import sys

# Add parent directory to path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import SessionLocal
from app.models.models import User

db = SessionLocal()

user_id = 'ae398ec8-b093-4506-8a1c-b97572855ce7'
user = db.query(User).filter(User.id == user_id).first()

if user:
    print(f"Name: {user.name}")
    print(f"Phone: {user.phone_number}")
    print(f"Company: {user.company_name}")
    print(f"Department: {user.department_name}")
    print(f"Contractor: {user.contractor_name}")
    print(f"Emergency Contact: {user.emergency_contact_name}")
    print(f"Emergency Phone: {user.emergency_contact_phone}")
else:
    print("User not found.")
