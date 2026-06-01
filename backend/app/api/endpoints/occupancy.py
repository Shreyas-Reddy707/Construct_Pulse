from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Site, User, Attendance, AttendanceStatus, Department, Contractor
from app.api.deps import get_current_user

router = APIRouter()

def compute_occupancy(site_id: str, db: Session):
    active_attendances = db.query(Attendance).filter(
        Attendance.site_id == site_id,
        Attendance.status == AttendanceStatus.CHECKED_IN
    ).all()
    
    total = len(active_attendances)
    dept_breakdown = {}
    contractor_breakdown = {}
    
    for att in active_attendances:
        user = att.user
        
        # Dept
        dept_id = user.department_id
        if dept_id:
            dept = db.query(Department).filter(Department.id == dept_id).first()
            if dept:
                dept_breakdown[dept.name] = dept_breakdown.get(dept.name, 0) + 1
                
        # Contractor
        cont_id = user.contractor_id
        if cont_id:
            cont = db.query(Contractor).filter(Contractor.id == cont_id).first()
            if cont:
                contractor_breakdown[cont.name] = contractor_breakdown.get(cont.name, 0) + 1
                
    return {
        "total_workers": total,
        "department_breakdown": dept_breakdown,
        "contractor_breakdown": contractor_breakdown
    }

@router.get("/current", response_model=List[schemas.OccupancyResponse])
def get_current_occupancy(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sites = db.query(Site).all()
    results = []
    for site in sites:
        occ = compute_occupancy(site.id, db)
        results.append(occ)
    return results

@router.get("/site/{site_id}", response_model=schemas.OccupancyResponse)
def get_site_occupancy(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return compute_occupancy(site_id, db)

@router.get("/departments/{site_id}")
def get_departments_occupancy(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    occ = compute_occupancy(site_id, db)
    return occ["department_breakdown"]

@router.get("/contractors/{site_id}")
def get_contractors_occupancy(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    occ = compute_occupancy(site_id, db)
    return occ["contractor_breakdown"]
