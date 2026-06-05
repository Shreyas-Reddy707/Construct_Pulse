import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.models.models import User, Company, WorkerStatus, UserRole

def fix_statuses():
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        for company in companies:
            workers = db.query(User).filter_by(company_id=company.id, role=UserRole.WORKER).all()
            
            # Count current
            approved = [w for w in workers if w.status == WorkerStatus.APPROVED]
            pending = [w for w in workers if w.status == WorkerStatus.PENDING]
            suspended = [w for w in workers if w.status == WorkerStatus.SUSPENDED]
            rejected = [w for w in workers if w.status == WorkerStatus.REJECTED]
            
            # Target
            # We want at least 2 pending, 2 suspended, 1 rejected. 
            target_pending = 2
            target_suspended = 2
            target_rejected = 1
            
            # Force target counts if they are not met
            needed_pending = target_pending - len(pending)
            needed_suspended = target_suspended - len(suspended)
            needed_rejected = target_rejected - len(rejected)
            
            # Convert approved to other statuses if needed
            available_for_conversion = [w for w in approved if 'Admin' not in w.name]
            
            for _ in range(needed_pending):
                if available_for_conversion:
                    w = available_for_conversion.pop()
                    w.status = WorkerStatus.PENDING
                    w.is_active = True
            
            for _ in range(needed_suspended):
                if available_for_conversion:
                    w = available_for_conversion.pop()
                    w.status = WorkerStatus.SUSPENDED
                    w.is_active = False
            
            for _ in range(needed_rejected):
                if available_for_conversion:
                    w = available_for_conversion.pop()
                    w.status = WorkerStatus.REJECTED
                    w.is_active = False

            db.commit()
            print(f"Company {company.company_name} statuses fixed.")
            
    finally:
        db.close()

if __name__ == "__main__":
    fix_statuses()
