import sys
import os

# Add the backend directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.models import User, UserRole, WorkerStatus

def bootstrap_admin(phone_number: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            print(f"User with phone number {phone_number} not found. Please register them in the app first.")
            return

        if user.role == UserRole.COMPANY_ADMIN:
            print(f"User {user.name} ({phone_number}) is already a COMPANY_ADMIN.")
            return

        user.role = UserRole.COMPANY_ADMIN
        user.status = WorkerStatus.APPROVED
        user.is_active = True
        
        db.commit()
        print(f"Success! User {user.name} ({phone_number}) has been promoted to COMPANY_ADMIN.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bootstrap_admin.py <phone_number>")
        sys.exit(1)
        
    target_phone = sys.argv[1]
    bootstrap_admin(target_phone)
