import asyncio
import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
import json

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.core.utils import normalize_phone_number

from app.db.database import SessionLocal
from app.models.models import (
    User, Company, Site, Attendance, Department, Contractor,
    UserRole, WorkerStatus, AttendanceStatus, SiteQRCode, OccupancySnapshot,
    worker_to_site, department_to_site, contractor_to_site
)

def seed_limelite_data(db: Session):
    print("--- STEP 2: REMOVE EXISTING DEMO DATA ---")
    
    from sqlalchemy import text
    db.execute(text("TRUNCATE TABLE worker_to_site, department_to_site, contractor_to_site, occupancy_snapshots, attendances, site_qr_codes, sites, users, departments, contractors, companies CASCADE;"))
    db.commit()

    print("--- STEP 3: CREATE COMPANY ---")
    company = Company(
        company_name="Limelite Construction",
        registration_number="REG-LIME-2026",
        contact_email="nilesh@limelite.co.nz",
        contact_phone="021 286 9009 / 03 925 9705"
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    print(f"Created company: {company.company_name}")

    print("--- STEP 4: CREATE COMPANY ADMIN ---")
    admin = User(
        name="Nilesh Patel",
        phone_number=normalize_phone_number("+640212869009"),
        role=UserRole.COMPANY_ADMIN,
        status=WorkerStatus.APPROVED,
        company_id=company.id,
        employee_id="EMP-LIME-001",
        is_active=True
    )
    db.add(admin)
    db.commit()

    print("--- STEP 5: CREATE DEPARTMENTS ---")
    dept_names = [
        "Administration", "Project Management", "Site Management", 
        "Health & Safety", "Procurement", "Engineering", 
        "Architecture", "Accounts", "Quality Assurance"
    ]
    departments = {}
    for dname in dept_names:
        dept = Department(company_id=company.id, name=dname, description=f"{dname} Department")
        db.add(dept)
        departments[dname] = dept
    db.commit()

    print("--- STEP 6 & 7: IMPORT CONTRACTORS AND WORKERS ---")
    with open('../contractors_fixed.json', 'r') as f:
        contractors_data = json.load(f)
    
    contractor_count = 0
    worker_count = 0

    for c_data in contractors_data:
        contractor = Contractor(
            company_id=company.id, 
            name=c_data["company"], 
            phone=c_data["phone"], 
            trade=c_data["trade"]
        )
        db.add(contractor)
        db.commit()
        db.refresh(contractor)
        contractor_count += 1
        
        if c_data["contact_name"]:
            dept = random.choice(list(departments.values()))
            worker_phone = c_data["phone"]
            worker_name = c_data["contact_name"].replace("-", "").strip()
            worker = User(
                name=worker_name,
                phone_number=normalize_phone_number(worker_phone) if worker_phone else None,
                role=UserRole.WORKER,
                status=WorkerStatus.APPROVED,
                company_id=company.id,
                employee_id=f"EMP-{uuid.uuid4().hex[:4].upper()}",
                department_id=dept.id,
                contractor_id=contractor.id,
                is_active=True
            )
            # No random regeneration of phones
            db.add(worker)
            worker_count += 1

    db.commit()

    print("--- STEP 8 & 11: SITES AND QR CODES ---")
    site_configs = [
        {"name": "Architectural Build - Fendalton", "address": "15 Fendalton Road, Christchurch", "lat": -43.518, "lon": 172.597, "radius": 75.0},
        {"name": "Townhouse Development - Riccarton", "address": "100 Riccarton Road, Christchurch", "lat": -43.531, "lon": 172.596, "radius": 100.0},
        {"name": "House & Land Package - Rolleston", "address": "50 Rolleston Drive, Christchurch", "lat": -43.593, "lon": 172.383, "radius": 75.0},
        {"name": "Residential Development - Halswell", "address": "200 Halswell Junction Road, Christchurch", "lat": -43.582, "lon": 172.571, "radius": 200.0}
    ]
    sites = []
    
    for config in site_configs:
        site = Site(
            company_id=company.id,
            name=config["name"],
            address=config["address"],
            latitude=config["lat"],
            longitude=config["lon"],
            geofence_radius_meters=config["radius"],
            status="active"
        )
        db.add(site)
        db.commit()
        db.refresh(site)
        sites.append(site)
        
        qr = SiteQRCode(
            site_id=site.id,
            qr_token=str(uuid.uuid4()),
            expires_at=datetime.now(timezone.utc) + timedelta(days=365)
        )
        db.add(qr)
    db.commit()
    
    print("--- ASSIGN WORKERS TO SITES ---")
    all_workers = db.query(User).filter_by(role=UserRole.WORKER).all()
    for worker in all_workers:
        assigned = random.sample(sites, k=random.randint(1, len(sites)))
        worker.assigned_sites.extend(assigned)
    
    # Assign the admin/supervisor to all sites so they show up dynamically in the frontend
    admin.assigned_sites.extend(sites)
    db.commit()

    print("--- STEP 9: ATTENDANCE ---")
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    attendance_count = 0
    
    for worker in all_workers:
        if not worker.assigned_sites: continue
        
        for day_offset in range(30):
            current_day = today - timedelta(days=day_offset)
            
            rand = random.random()
            if rand < 0.05:
                status = AttendanceStatus.ABSENT
                att = Attendance(
                    user_id=worker.id, site_id=worker.assigned_sites[0].id,
                    company_id=company.id, check_in_time=current_day.replace(hour=8),
                    status=status
                )
                db.add(att)
                attendance_count += 1
                continue
                
            site = random.choice(worker.assigned_sites)
            
            check_in_hour = random.randint(7, 9) if rand > 0.1 else random.randint(10, 11)
            check_in_minute = random.randint(0, 59)
            check_in_time = current_day.replace(hour=check_in_hour, minute=check_in_minute)
            
            if day_offset == 0 and random.random() < 0.5:
                check_out_time = None
                status = AttendanceStatus.CHECKED_IN
            else:
                check_out_hour = random.randint(16, 20)
                check_out_minute = random.randint(0, 59)
                check_out_time = current_day.replace(hour=check_out_hour, minute=check_out_minute)
                status = AttendanceStatus.CHECKED_OUT
                
            att = Attendance(
                user_id=worker.id, site_id=site.id, company_id=company.id,
                check_in_time=check_in_time, check_out_time=check_out_time,
                gps_latitude=site.latitude, gps_longitude=site.longitude,
                status=status
            )
            db.add(att)
            attendance_count += 1
    db.commit()

    print("--- STEP 10: OCCUPANCY SNAPSHOTS ---")
    for site in sites:
        for hour in range(8, 18, 2):
            snap_time = today.replace(hour=hour)
            checked_in = db.query(Attendance).filter(
                Attendance.site_id == site.id,
                Attendance.check_in_time <= snap_time,
                or_(Attendance.check_out_time == None, Attendance.check_out_time > snap_time)
            ).all()
            
            dept_breakdown = {}
            contractor_breakdown = {}
            for att in checked_in:
                if att.user.department:
                    dept_breakdown[att.user.department.name] = dept_breakdown.get(att.user.department.name, 0) + 1
                if att.user.contractor:
                    contractor_breakdown[att.user.contractor.name] = contractor_breakdown.get(att.user.contractor.name, 0) + 1
                    
            snap = OccupancySnapshot(
                site_id=site.id,
                timestamp=snap_time,
                total_workers=len(checked_in),
                department_breakdown=dept_breakdown,
                contractor_breakdown=contractor_breakdown
            )
            db.add(snap)
    db.commit()

    print("\n--- SEEDING COMPLETE ---")
    print(f"Summary:")
    print(f"  Companies: 1")
    print(f"  Departments: {len(departments)}")
    print(f"  Contractors: {contractor_count}")
    print(f"  Workers: {worker_count}")
    print(f"  Sites: {len(sites)}")
    print(f"  Attendance Records: {attendance_count}")
    
    print("\nTODO (Step 13): The database schema currently doesn't have an explicit field for User Profile Image or Company Logo Image URLs. These assets are ready in the repository but have been omitted to preserve schema architecture.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_limelite_data(db)
    finally:
        db.close()
