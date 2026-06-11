import asyncio
from app.db.database import SessionLocal
from app.models.models import User, WorkerStatus

def check_pending():
    db = SessionLocal()
    pending_users = db.query(User).filter(User.status == WorkerStatus.PENDING).all()
    print("Pending DB count:", len(pending_users))
    for u in pending_users:
        print(f"User ID: {u.id}, role: {u.role}, company_id: {u.company_id}, status: {u.status}, is_active: {u.is_active}")

check_pending()
