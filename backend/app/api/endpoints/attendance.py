from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
import math
from app.db.database import get_db
from app.schemas import schemas
from app.models.models import Site, User, Attendance, SiteQRCode, AttendanceStatus
from app.api.deps import get_current_user

router = APIRouter()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # radius of earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    meters = R * c
    return meters

@router.post("/check-in", response_model=schemas.AttendanceResponse)
def check_in(checkin_data: schemas.AttendanceCheckIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    site = db.query(Site).filter(Site.id == checkin_data.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
        
    # Verify worker belongs to company
    if site.company_id and current_user.company_id and site.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Worker does not belong to the site's company")
    
    # Verify worker assigned
    if not any(w.id == current_user.id for w in site.assigned_workers):
        raise HTTPException(status_code=403, detail="Worker not assigned to this site")
    
    # Verify QR valid
    qr = db.query(SiteQRCode).filter(SiteQRCode.qr_token == checkin_data.qr_token, SiteQRCode.site_id == site.id).first()
    expires_at = qr.expires_at.replace(tzinfo=timezone.utc) if qr.expires_at.tzinfo is None else qr.expires_at
    if not qr or expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired QR code")
    
    # Validate GPS
    if site.latitude is not None and site.longitude is not None:
        distance = haversine(site.latitude, site.longitude, checkin_data.gps_latitude, checkin_data.gps_longitude)
        if distance > site.geofence_radius_meters:
            raise HTTPException(status_code=400, detail=f"Outside geofence. Distance: {distance:.2f}m")
    
    # Check if already checked in at ANY site
    existing = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.status == AttendanceStatus.CHECKED_IN
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already has an active check-in")
        
    attendance = Attendance(
        user_id=current_user.id,
        site_id=site.id,
        company_id=current_user.company_id,
        gps_latitude=checkin_data.gps_latitude,
        gps_longitude=checkin_data.gps_longitude,
        status=AttendanceStatus.CHECKED_IN
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.post("/check-out", response_model=schemas.AttendanceResponse)
def check_out(checkout_data: schemas.AttendanceCheckOut, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attendance = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.site_id == checkout_data.site_id,
        Attendance.status == AttendanceStatus.CHECKED_IN
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="Active check-in not found")
    
    site = db.query(Site).filter(Site.id == checkout_data.site_id).first()
    
    # Validate GPS for checkout too
    if site and site.latitude is not None and site.longitude is not None:
        distance = haversine(site.latitude, site.longitude, checkout_data.gps_latitude, checkout_data.gps_longitude)
        if distance > site.geofence_radius_meters:
            raise HTTPException(status_code=400, detail=f"Outside geofence. Distance: {distance:.2f}m")
            
    attendance.check_out_time = datetime.now(timezone.utc)
    attendance.status = AttendanceStatus.CHECKED_OUT
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/worker/{worker_id}", response_model=List[schemas.AttendanceResponse])
def get_worker_attendance(worker_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Attendance).filter(Attendance.user_id == worker_id)
    if current_user.company_id:
        query = query.filter(Attendance.company_id == current_user.company_id)
    return query.all()

@router.get("/site/{site_id}", response_model=List[schemas.AttendanceResponse])
def get_site_attendance(site_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Attendance).filter(Attendance.site_id == site_id)
    if current_user.company_id:
        query = query.filter(Attendance.company_id == current_user.company_id)
    return query.all()
