import asyncio
import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from faker import Faker

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.models.models import (
    User, Company, Site, Attendance, Department, Contractor,
    UserRole, WorkerStatus, AttendanceStatus
)

fake = Faker()

def generate_phone():
    return f"+1{fake.numerify('##########')}"

def repair_data(db: Session):
    print("--- PHASE A: DATA QUALITY REPAIR ---")
    repaired = {"User": 0, "Company": 0, "Site": 0, "Attendance": 0, "Department": 0, "Contractor": 0}

    # Repair Companies
    for company in db.query(Company).all():
        changed = False
        if not company.contact_email: company.contact_email = fake.company_email(); changed = True
        if not company.contact_phone: company.contact_phone = generate_phone(); changed = True
        if not company.registration_number: company.registration_number = fake.bothify('REG-####-????'); changed = True
        if changed: repaired["Company"] += 1

    db.commit()

    # Repair Departments
    for dept in db.query(Department).all():
        changed = False
        if not dept.description: dept.description = fake.catch_phrase(); changed = True
        if changed: repaired["Department"] += 1

    db.commit()

    # Repair Contractors
    for contractor in db.query(Contractor).all():
        changed = False
        if not contractor.phone: contractor.phone = generate_phone(); changed = True
        if not contractor.trade: contractor.trade = random.choice(["Civil", "Electrical", "Plumbing"]); changed = True
        if changed: repaired["Contractor"] += 1

    db.commit()

    # Repair Sites
    for site in db.query(Site).all():
        changed = False
        if not site.address: site.address = fake.address(); changed = True
        if site.latitude is None: site.latitude = float(fake.latitude()); changed = True
        if site.longitude is None: site.longitude = float(fake.longitude()); changed = True
        if changed: repaired["Site"] += 1

    db.commit()

    # Repair Users
    companies = db.query(Company).all()
    if not companies:
        company = Company(company_name="Default Company", contact_email="contact@default.com", contact_phone="+10000000000")
        db.add(company)
        db.commit()
        db.refresh(company)
        companies = [company]

    for user in db.query(User).all():
        changed = False
        if not user.name: user.name = fake.name(); changed = True
        if not user.employee_id: user.employee_id = fake.bothify('EMP-####'); changed = True
        if not user.phone_number: user.phone_number = generate_phone(); changed = True
        if not user.company_id: user.company_id = random.choice(companies).id; changed = True
        if not user.emergency_contact_name: user.emergency_contact_name = fake.name(); changed = True
        if not user.emergency_contact_phone: user.emergency_contact_phone = generate_phone(); changed = True
        if not user.emergency_contact_relationship: user.emergency_contact_relationship = random.choice(["Spouse", "Parent", "Sibling", "Friend"]); changed = True
        
        # We'll assign dept and contractor later in the script for new users, but let's just make sure they have it if we create them
        if changed: repaired["User"] += 1

    db.commit()

    # Repair Attendances
    for att in db.query(Attendance).all():
        changed = False
        if not att.company_id and att.site_id:
            site = db.query(Site).filter(Site.id == att.site_id).first()
            if site:
                att.company_id = site.company_id
                changed = True
        if changed: repaired["Attendance"] += 1

    db.commit()

    for k, v in repaired.items():
        print(f"Repaired {v} {k} records.")

def seed_data(db: Session):
    print("\n--- PHASE B to H: SEEDING NEW DATA ---")
    
    # PHASE B: COMPANY EXPANSION
    # We need 4 companies total
    existing_companies = db.query(Company).all()
    needed_companies = max(0, 4 - len(existing_companies))
    for _ in range(needed_companies):
        company = Company(
            company_name=fake.company(),
            registration_number=fake.bothify('REG-####-????'),
            contact_email=fake.company_email(),
            contact_phone=generate_phone()
        )
        db.add(company)
    db.commit()
    
    companies = db.query(Company).all()[:4] # Take exactly 4

    total_records = {"Company": len(companies), "Department": 0, "Contractor": 0, "Site": 0, "User": 0, "Attendance": 0}

    for company in companies:
        print(f"\nProcessing Company: {company.company_name}")
        
        # PHASE C: DEPARTMENTS
        dept_names = ["Civil Works", "Electrical", "Plumbing", "Safety", "Quality Control", "Site Operations"]
        dept_map = {}
        for dname in dept_names:
            dept = db.query(Department).filter_by(company_id=company.id, name=dname).first()
            if not dept:
                dept = Department(company_id=company.id, name=dname, description=f"{dname} Department")
                db.add(dept)
                total_records["Department"] += 1
            dept_map[dname] = dept
        db.commit()

        # PHASE D: CONTRACTORS
        contractor_names = ["ABC Constructions", "Metro Infra", "Skyline Projects", "Prime Engineering", "Urban Build Solutions"]
        contractor_map = {}
        for cname in contractor_names:
            contractor = db.query(Contractor).filter_by(company_id=company.id, name=cname).first()
            if not contractor:
                contractor = Contractor(company_id=company.id, name=cname, phone=generate_phone(), trade="General")
                db.add(contractor)
                total_records["Contractor"] += 1
            contractor_map[cname] = contractor
        db.commit()

        # PHASE E: SITE CREATION
        sites = db.query(Site).filter_by(company_id=company.id).all()
        needed_sites = max(0, 3 - len(sites))
        for _ in range(needed_sites):
            site = Site(
                company_id=company.id,
                name=f"Site - {fake.city()}",
                address=fake.address(),
                latitude=float(fake.latitude()),
                longitude=float(fake.longitude()),
                geofence_radius_meters=100.0,
                status="active"
            )
            db.add(site)
            total_records["Site"] += 1
        db.commit()
        sites = db.query(Site).filter_by(company_id=company.id).all()

        # PHASE B: USERS
        # Target: 1 Admin, 1 Site Manager, 15 Workers
        admins = db.query(User).filter_by(company_id=company.id, role=UserRole.COMPANY_ADMIN).all()
        if not admins:
            admin = User(name=fake.name(), phone_number=generate_phone(), role=UserRole.COMPANY_ADMIN, status=WorkerStatus.APPROVED, company_id=company.id, employee_id=fake.bothify('EMP-####'))
            db.add(admin)
            total_records["User"] += 1
            
        managers = db.query(User).filter_by(company_id=company.id, role=UserRole.SUPERVISOR).all()
        if not managers:
            manager = User(name=fake.name(), phone_number=generate_phone(), role=UserRole.SUPERVISOR, status=WorkerStatus.APPROVED, company_id=company.id, employee_id=fake.bothify('EMP-####'))
            db.add(manager)
            total_records["User"] += 1
            
        existing_workers = db.query(User).filter_by(company_id=company.id, role=UserRole.WORKER).all()
        needed_workers = max(0, 15 - len(existing_workers))
        
        # PHASE H: WORKFORCE STATES (10 Approved, 2 Pending, 2 Suspended, 1 Rejected)
        # We will just assign statuses for the new workers to reach this distribution or just distribute over all 15.
        statuses = [WorkerStatus.APPROVED]*10 + [WorkerStatus.PENDING]*2 + [WorkerStatus.SUSPENDED]*2 + [WorkerStatus.REJECTED]*1
        
        # Departments distribution: Civil:5, Electrical:3, Plumbing:2, Safety:2, Quality:1, Operations:2
        dept_assignment = (
            [dept_map["Civil Works"]]*5 +
            [dept_map["Electrical"]]*3 +
            [dept_map["Plumbing"]]*2 +
            [dept_map["Safety"]]*2 +
            [dept_map["Quality Control"]]*1 +
            [dept_map["Site Operations"]]*2
        )
        
        new_workers = []
        for i in range(needed_workers):
            status = statuses[i] if i < len(statuses) else WorkerStatus.APPROVED
            dept = dept_assignment[i] if i < len(dept_assignment) else dept_map["Civil Works"]
            contractor = contractor_map[random.choice(contractor_names)]
            
            worker = User(
                name=fake.name(),
                phone_number=generate_phone(),
                role=UserRole.WORKER,
                status=status,
                company_id=company.id,
                employee_id=fake.bothify('EMP-####'),
                department_id=dept.id,
                contractor_id=contractor.id,
                emergency_contact_name=fake.name(),
                emergency_contact_phone=generate_phone(),
                emergency_contact_relationship=random.choice(["Spouse", "Parent", "Sibling", "Friend"])
            )
            db.add(worker)
            new_workers.append(worker)
            total_records["User"] += 1
            
        db.commit()
        
        # Assign to sites
        all_workers = db.query(User).filter_by(company_id=company.id, role=UserRole.WORKER).all()
        for worker in all_workers:
            # Clear existing sites
            worker.assigned_sites.clear()
            # Assign 1 to 2 random sites
            assigned = random.sample(sites, k=random.randint(1, min(2, len(sites))))
            worker.assigned_sites.extend(assigned)
        db.commit()

        # PHASE F: ATTENDANCE HISTORY
        # 30 days of history for 15 workers -> ~450 records per company -> ~1800 total
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Ensure we only generate for the 15 workers (or all workers if more)
        for worker in all_workers:
            if not worker.assigned_sites:
                continue
                
            for day_offset in range(30):
                current_day = today - timedelta(days=day_offset)
                
                # Randomize attendance: 80% present, 20% absent
                if random.random() < 0.2:
                    continue
                    
                site = random.choice(worker.assigned_sites)
                
                # Check in between 7:00 and 9:30
                check_in_hour = random.randint(7, 9)
                check_in_minute = random.randint(0, 59)
                check_in_time = current_day.replace(hour=check_in_hour, minute=check_in_minute)
                
                # Current day: Some are still checked in
                if day_offset == 0 and random.random() < 0.5:
                    check_out_time = None
                    status = AttendanceStatus.CHECKED_IN
                else:
                    # Check out between 16:00 and 20:00
                    check_out_hour = random.randint(16, 20)
                    check_out_minute = random.randint(0, 59)
                    check_out_time = current_day.replace(hour=check_out_hour, minute=check_out_minute)
                    status = AttendanceStatus.CHECKED_OUT
                
                # Check if attendance already exists for this day to avoid duplicate seeding if run multiple times
                existing_att = db.query(Attendance).filter(
                    Attendance.user_id == worker.id,
                    Attendance.check_in_time >= current_day,
                    Attendance.check_in_time < current_day + timedelta(days=1)
                ).first()
                
                if not existing_att:
                    att = Attendance(
                        user_id=worker.id,
                        site_id=site.id,
                        company_id=company.id,
                        check_in_time=check_in_time,
                        check_out_time=check_out_time,
                        gps_latitude=site.latitude,
                        gps_longitude=site.longitude,
                        status=status
                    )
                    db.add(att)
                    total_records["Attendance"] += 1
                    
        db.commit()

    print("\n--- SEEDING COMPLETE ---")
    for k, v in total_records.items():
        print(f"Created {v} new {k} records.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        repair_data(db)
        seed_data(db)
    finally:
        db.close()
