import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.models.models import Site, SiteQRCode
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

def run_audit():
    db = SessionLocal()
    
    sites = db.query(Site).options(
        joinedload(Site.assigned_workers)
    ).all()
    
    now = datetime.now(timezone.utc)
    
    print("=== QR READINESS AUDIT ===")
    
    for s in sites:
        qrs = db.query(SiteQRCode).filter(SiteQRCode.site_id == s.id).all()
        workers_count = len(s.assigned_workers)
        
        active_qrs = [qr for qr in qrs if qr.expires_at is None or qr.expires_at > now]
        latest_expiry = max([qr.expires_at for qr in qrs if qr.expires_at is not None], default=None)
        
        if workers_count > 0 and len(active_qrs) == 1:
            status = "READY"
        else:
            status = "BLOCKED"
            
        print(f"Site Name: {s.name}")
        print(f"Site ID: {s.id}")
        print(f"Assigned Worker Count: {workers_count}")
        print(f"Active QR Count: {len(active_qrs)}")
        print(f"Latest Expiry: {latest_expiry}")
        print(f"Status: {status}")
        print("-" * 30)

    db.close()

if __name__ == '__main__':
    run_audit()
