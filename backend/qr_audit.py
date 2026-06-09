import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath('.'))

from app.db.database import SessionLocal
from app.models.models import User, Site, SiteQRCode
from sqlalchemy.orm import joinedload

def run_audit():
    db = SessionLocal()
    
    sites = db.query(Site).options(
        joinedload(Site.assigned_workers)
    ).all()
    
    now = datetime.now(timezone.utc)
    
    print("=== SITE AUDIT ===")
    sites_workers_no_qr = []
    sites_qr_no_workers = []
    expired_qrs_total = 0
    duplicate_qrs_total = 0

    for s in sites:
        qrs = db.query(SiteQRCode).filter(SiteQRCode.site_id == s.id).all()
        workers_count = len(s.assigned_workers)
        active_qrs = [qr for qr in qrs if (qr.expires_at is None or qr.expires_at > now)]
        expired_qrs = [qr for qr in qrs if (qr.expires_at is not None and qr.expires_at <= now)]
        latest_expiry = max([qr.expires_at for qr in qrs if qr.expires_at is not None], default=None)
        
        expired_qrs_total += len(expired_qrs)
        if len(active_qrs) > 1:
            duplicate_qrs_total += (len(active_qrs) - 1)
            
        if workers_count > 0 and not active_qrs:
            sites_workers_no_qr.append(s.name)
        if len(active_qrs) > 0 and workers_count == 0:
            sites_qr_no_workers.append(s.name)
            
        print(f"Site ID: {s.id}")
        print(f"Site Name: {s.name}")
        print(f"Assigned Workers: {workers_count}")
        print(f"Active QRs: {len(active_qrs)}")
        print(f"Latest Expiry: {latest_expiry}")
        print("-" * 20)

    print("\n=== IDENTIFICATIONS ===")
    print(f"Sites with workers but no active QR: {', '.join(sites_workers_no_qr) or 'None'}")
    print(f"Sites with QR but no workers: {', '.join(sites_qr_no_workers) or 'None'}")
    print(f"Expired QR codes found: {expired_qrs_total}")
    print(f"Duplicate active QR codes found: {duplicate_qrs_total}")

    print("\n=== DEMO WORKERS AUDIT ===")
    demo_workers = db.query(User).filter(User.role == 'WORKER').all()
    
    henry = next((w for w in demo_workers if w.name == 'Henry Sullivan'), None)
    if henry:
        assigned_sites = [s for s in sites if any(aw.id == henry.id for aw in s.assigned_workers)]
        print(f"Worker: {henry.name} ({henry.phone_number})")
        if not assigned_sites:
            print("  Assigned Sites: NONE")
        for s in assigned_sites:
            qrs = db.query(SiteQRCode).filter(SiteQRCode.site_id == s.id).all()
            active_qrs = [qr for qr in qrs if (qr.expires_at is None or qr.expires_at > now)]
            print(f"  Assigned Site: {s.name}")
            print(f"  Valid QR Available: {'YES' if active_qrs else 'NO'}")
            
    db.close()

if __name__ == '__main__':
    run_audit()
