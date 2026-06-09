import sys
import os
from datetime import timedelta
sys.path.append(os.path.abspath('.'))

from app.db.database import SessionLocal
from app.models.models import SiteQRCode

db = SessionLocal()

# Find all QRs where expires_at is None
qrs = db.query(SiteQRCode).filter(SiteQRCode.expires_at == None).all()
print(f"Found {len(qrs)} QRs with expires_at = NULL.")

for qr in qrs:
    qr.expires_at = qr.created_at + timedelta(days=365)
    
db.commit()
print("Data cleanup complete.")

