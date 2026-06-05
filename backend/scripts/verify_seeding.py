import os
import sys
from datetime import datetime, timezone
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.models.models import User, Company, Site, Attendance, Department, Contractor
from sqlalchemy import func

def verify_data():
    db = SessionLocal()
    try:
        print("--- SEEDING VERIFICATION ---")
        
        # Breakdown by company
        companies = db.query(Company).all()
        print(f"\nTotal Companies: {len(companies)}")
        
        for company in companies:
            print(f"\nCompany: {company.company_name}")
            workers = db.query(User).filter_by(company_id=company.id).count()
            sites = db.query(Site).filter_by(company_id=company.id).count()
            depts = db.query(Department).filter_by(company_id=company.id).count()
            contractors = db.query(Contractor).filter_by(company_id=company.id).count()
            attendances = db.query(Attendance).filter_by(company_id=company.id).count()
            print(f"  Workers: {workers}")
            print(f"  Sites: {sites}")
            print(f"  Departments: {depts}")
            print(f"  Contractors: {contractors}")
            print(f"  Attendance Records: {attendances}")
            
            # Workforce States
            approved = db.query(User).filter_by(company_id=company.id, status="APPROVED").count()
            pending = db.query(User).filter_by(company_id=company.id, status="PENDING").count()
            suspended = db.query(User).filter_by(company_id=company.id, status="SUSPENDED").count()
            rejected = db.query(User).filter_by(company_id=company.id, status="REJECTED").count()
            
            print(f"  Statuses -> Approved: {approved}, Pending: {pending}, Suspended: {suspended}, Rejected: {rejected}")
            
            # Dashboard metrics verification
            today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            
            workers_on_site = db.query(Attendance).filter(
                Attendance.company_id == company.id,
                Attendance.check_out_time.is_(None)
            ).count()
            
            checked_in_today = db.query(Attendance).filter(
                Attendance.company_id == company.id,
                Attendance.check_in_time >= today
            ).count()
            
            checked_out_today = db.query(Attendance).filter(
                Attendance.company_id == company.id,
                Attendance.check_in_time >= today,
                Attendance.check_out_time.isnot(None)
            ).count()
            
            print(f"  Dashboard -> On Site: {workers_on_site}, Checked In Today: {checked_in_today}, Checked Out Today: {checked_out_today}")
            
        print("\n--- SAMPLE SQL QUERIES ---")
        
        # 1. Dashboard queries
        print("\nQuery: Workers On Site")
        print("SELECT count(id) FROM attendances WHERE check_out_time IS NULL AND company_id = ?;")
        
        print("\nQuery: Checked In Today")
        print("SELECT count(id) FROM attendances WHERE check_in_time >= current_date() AND company_id = ?;")
        
        # 2. Export query
        print("\nQuery: Export CSV")
        print('''
SELECT 
    u.name as worker_name, 
    u.employee_id, 
    c.company_name, 
    d.name as department, 
    con.name as contractor,
    s.name as site, 
    a.check_in_time, 
    a.check_out_time
FROM attendances a
JOIN users u ON a.user_id = u.id
LEFT JOIN companies c ON u.company_id = c.id
LEFT JOIN departments d ON u.department_id = d.id
LEFT JOIN contractors con ON u.contractor_id = con.id
LEFT JOIN sites s ON a.site_id = s.id
ORDER BY a.check_in_time DESC
LIMIT 5;
        ''')
        
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()
