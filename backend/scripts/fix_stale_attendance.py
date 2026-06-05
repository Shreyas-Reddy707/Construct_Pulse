import os
import sys
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import SessionLocal
from app.models.models import Attendance, AttendanceStatus

db = SessionLocal()
yesterday = datetime.now(timezone.utc) - timedelta(hours=24)

stale_records = db.query(Attendance).filter(
    Attendance.status == AttendanceStatus.CHECKED_IN,
    Attendance.check_in_time < yesterday
).all()

count = 0
for record in stale_records:
    record.status = AttendanceStatus.CHECKED_OUT
    if record.check_in_time:
        record.check_out_time = record.check_in_time + timedelta(hours=8)
    count += 1

db.commit()
print(f"Fixed {count} stale attendance records.")
