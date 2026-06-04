import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.models import User, UserRole, WorkerStatus

def bootstrap_system_admin(phone_number: str):
    url = settings.DATABASE_URL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://")
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            print(f"Error: User with phone number {phone_number} not found.")
            sys.exit(1)
            
        user.role = UserRole.SYSTEM_ADMIN
        user.status = WorkerStatus.APPROVED
        user.is_active = True
        
        db.commit()
        db.refresh(user)
        
        print(f"Success: User {user.name} ({user.phone_number}) is now SYSTEM_ADMIN.")
        print(f"ID: {user.id}")
        print(f"Role: {user.role.value}")
        print(f"Status: {user.status.value}")
        print(f"Active: {user.is_active}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bootstrap_system_admin.py <phone_number>")
        sys.exit(1)
        
    phone_number = sys.argv[1]
    bootstrap_system_admin(phone_number)
