from datetime import date, datetime, timezone, timedelta
from sqlalchemy import cast, Date
from app.db.database import SessionLocal
from app.models.models import Attendance

db = SessionLocal()

today_utc = datetime.now(timezone.utc).date()
yesterday_utc = datetime.now(timezone.utc) - timedelta(hours=24)

q_checked_in = db.query(Attendance).filter(cast(Attendance.check_in_time, Date) == today_utc)
print("checked_in_today:", q_checked_in.count())

q_on_site = db.query(Attendance).filter(Attendance.check_out_time == None, Attendance.status == "checked_in", Attendance.check_in_time >= yesterday_utc)
print("on_site:", q_on_site.count())

