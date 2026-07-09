from sqlalchemy.orm import Session
from app.models.models import Site, SiteQRCode, UserRole
from typing import List, Dict

class SiteReadinessService:
    @classmethod
    def evaluate(cls, site: Site, session: Session) -> dict:
        missing_requirements = cls.missing_requirements(site, session)
        return {
            "status": site.status.value if hasattr(site.status, "value") else site.status,
            "ready": len(missing_requirements) == 0,
            "missing": missing_requirements
        }

    @classmethod
    def update_lifecycle_state(cls, site: Site, session: Session):
        from app.models.models import SiteStatus
        ready = cls.is_ready(site, session)
        if site.status == SiteStatus.DRAFT and ready:
            site.status = SiteStatus.CONFIGURED
        elif site.status == SiteStatus.CONFIGURED and not ready:
            site.status = SiteStatus.DRAFT

    @classmethod
    def is_ready(cls, site: Site, session: Session) -> bool:
        return len(cls.missing_requirements(site, session)) == 0

    @classmethod
    def missing_requirements(cls, site: Site, session: Session) -> List[Dict[str, str]]:
        missing = []
        
        # 1. Company exists
        if not site.company_id:
            missing.append({"code": "SITE_MISSING_COMPANY", "message": "Site must belong to a company."})
            
        # 2. Site name
        if not site.name:
            missing.append({"code": "SITE_MISSING_NAME", "message": "Site name must be provided."})
            
        # 3. GPS coordinates
        if site.latitude is None or site.longitude is None:
            missing.append({"code": "SITE_MISSING_GPS", "message": "Site must have valid GPS coordinates."})
            
        # 4. Attendance radius
        if site.geofence_radius_meters is None or site.geofence_radius_meters <= 0:
            missing.append({"code": "SITE_MISSING_RADIUS", "message": "Site must have a valid attendance radius."})
            
        # 5. Site Manager assigned
        has_manager = any(w.role == UserRole.SITE_MANAGER for w in site.assigned_workers)
        if not has_manager:
            missing.append({"code": "SITE_MISSING_MANAGER", "message": "Site must have at least one Site Manager assigned."})
            
        # 6. QR generated
        from datetime import datetime, timezone
        from sqlalchemy import or_
        now_utc = datetime.now(timezone.utc)
        
        active_qr = session.query(SiteQRCode).filter(
            SiteQRCode.site_id == site.id,
            or_(SiteQRCode.expires_at == None, SiteQRCode.expires_at > now_utc)
        ).first()
        
        if not active_qr:
            missing.append({"code": "SITE_MISSING_QR", "message": "Site must have an active QR code generated."})
            
        # 7. Primary emergency contact configured
        if not site.primary_emergency_contact_name or not site.primary_emergency_contact_phone:
            missing.append({"code": "SITE_MISSING_EMERGENCY_CONTACT", "message": "Site must have a primary emergency contact configured."})
            
        return missing
