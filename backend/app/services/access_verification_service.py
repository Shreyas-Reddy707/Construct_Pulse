from typing import List, Optional, Dict
from datetime import datetime, timezone
import math
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import (
    User, Site, SiteQRCode, Attendance, 
    AttendanceStatus, WorkerStatus, SiteStatus, UserRole
)
from app.schemas.schemas import AccessDecision, AccessRequirement
from app.services.worker_readiness_service import WorkerReadinessService
from app.services.site_readiness_service import SiteReadinessService


class AccessContext:
    def __init__(
        self, 
        session: Session, 
        user: User, 
        qr_token: Optional[str] = None, 
        gps_latitude: Optional[float] = None, 
        gps_longitude: Optional[float] = None,
        site: Optional[Site] = None
    ):
        self.session = session
        self.user = user
        self.qr_token = qr_token
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        
        self.site: Optional[Site] = site
        self.qr_record: Optional[SiteQRCode] = None
        self.trace: Dict[str, str] = {}
        self.reasons: List[AccessRequirement] = []

    def add_reason(self, code: str, message: str, severity: str = "ERROR"):
        self.reasons.append(AccessRequirement(code=code, message=message, severity=severity))

    def record_trace(self, step: str, result: str):
        self.trace[step] = result


class AccessVerificationService:
    """
    Central decision engine responsible for determining whether an individual is permitted
    to access a construction site. This service evaluates access eligibility and returns
    a structured decision without modifying database state or creating attendance records.
    """

    @classmethod
    def evaluate(
        cls,
        session: Session,
        user: User,
        qr_token: Optional[str] = None,
        gps_latitude: Optional[float] = None,
        gps_longitude: Optional[float] = None,
        site: Optional[Site] = None
    ) -> AccessDecision:
        context = AccessContext(
            session=session,
            user=user,
            qr_token=qr_token,
            gps_latitude=gps_latitude,
            gps_longitude=gps_longitude,
            site=site
        )

        # Validation Ordering:
        # Identity -> QR Resolution -> Site Resolution -> Site State -> Assignment -> Worker Readiness -> GPS Validation -> Duplicate Attendance -> Final Decision
        
        if not cls._check_identity(context):
            return cls._build_decision(context)
            
        if not cls._resolve_qr(context):
            return cls._build_decision(context)
            
        if not cls._resolve_site(context):
            return cls._build_decision(context)

        cls._check_site_state(context)
        cls._check_assignment(context)
        cls._check_worker_readiness(context)
        cls._check_gps(context)
        cls._check_duplicate_attendance(context)

        return cls._build_decision(context)

    @classmethod
    def is_allowed(
        cls,
        session: Session,
        user: User,
        qr_token: Optional[str] = None,
        gps_latitude: Optional[float] = None,
        gps_longitude: Optional[float] = None,
        site: Optional[Site] = None
    ) -> bool:
        decision = cls.evaluate(session, user, qr_token, gps_latitude, gps_longitude, site)
        return decision.allowed

    @classmethod
    def denial_reasons(
        cls,
        session: Session,
        user: User,
        qr_token: Optional[str] = None,
        gps_latitude: Optional[float] = None,
        gps_longitude: Optional[float] = None,
        site: Optional[Site] = None
    ) -> List[AccessRequirement]:
        decision = cls.evaluate(session, user, qr_token, gps_latitude, gps_longitude, site)
        return decision.reasons

    @classmethod
    def _check_identity(cls, context: AccessContext) -> bool:
        user = context.user
        passed = True
        
        if getattr(user, "is_deleted", False):
            context.add_reason(code="ACCESS_IDENTITY_DELETED", message="Worker account is deleted.", severity="CRITICAL")
            passed = False
        
        if user.status == WorkerStatus.PENDING:
            context.add_reason(code="ACCESS_WORKER_PENDING", message="Worker registration is pending approval.", severity="WARNING")
            passed = False
        elif user.status == WorkerStatus.SUSPENDED:
            context.add_reason(code="ACCESS_WORKER_SUSPENDED", message="Worker is currently suspended.", severity="CRITICAL")
            passed = False
            
        context.record_trace("Identity", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _resolve_qr(cls, context: AccessContext) -> bool:
        if not context.qr_token:
            if context.site:
                context.record_trace("QR Resolution", "SKIPPED (Site Pre-Resolved)")
                return True
                
            context.add_reason(code="ACCESS_MISSING_QR", message="A secure token is required for access.", severity="ERROR")
            context.record_trace("QR Resolution", "FAIL")
            return False
            
        from app.services.secure_token_service import SecureTokenService
        
        status = SecureTokenService.validate_token(context.session, context.qr_token)
        
        if status == "INVALID":
            context.add_reason(code="ACCESS_INVALID_TOKEN", message="The provided token is invalid.", severity="CRITICAL")
            context.record_trace("QR Resolution", "FAIL")
            return False
            
        if status == "REVOKED":
            context.add_reason(code="ACCESS_TOKEN_REVOKED", message="The provided token has been revoked.", severity="CRITICAL")
            context.record_trace("QR Resolution", "FAIL")
            return False
            
        if status == "EXPIRED":
            context.add_reason(code="ACCESS_TOKEN_EXPIRED", message="The provided token has expired.", severity="ERROR")
            context.record_trace("QR Resolution", "FAIL")
            return False
            
        context.record_trace("QR Resolution", "PASS")
        return True

    @classmethod
    def _resolve_site(cls, context: AccessContext) -> bool:
        if context.site:
            context.record_trace("Site Resolution", "PASS (PRE-RESOLVED)")
            return True
            
        if not context.qr_token:
            context.record_trace("Site Resolution", "FAIL")
            return False
            
        from app.services.secure_token_service import SecureTokenService
        site = SecureTokenService.resolve_site(context.session, context.qr_token)
        
        if not site:
            context.add_reason(code="ACCESS_SITE_NOT_FOUND", message="The associated site could not be found.", severity="CRITICAL")
            context.record_trace("Site Resolution", "FAIL")
            return False
            
        context.site = site
        context.record_trace("Site Resolution", "PASS")
        return True

    @classmethod
    def _check_site_state(cls, context: AccessContext) -> bool:
        site = context.site
        passed = True
        
        if site.status == SiteStatus.ARCHIVED:
            context.add_reason(code="ACCESS_SITE_ARCHIVED", message="Site is archived and cannot accept attendance.", severity="CRITICAL")
            passed = False
        elif site.status != SiteStatus.ACTIVE:
            context.add_reason(code="ACCESS_SITE_INACTIVE", message="Site is not active.", severity="ERROR")
            passed = False
            
        readiness = SiteReadinessService.evaluate(site, context.session)
        if not readiness.get("ready", False):
            context.add_reason(code="ACCESS_SITE_NOT_READY", message="Site has missing operational configurations.", severity="ERROR")
            passed = False
            
        context.record_trace("Site State", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _check_assignment(cls, context: AccessContext) -> bool:
        user = context.user
        site = context.site
        passed = True
        
        if site.company_id and user.company_id and site.company_id != user.company_id:
            context.add_reason(code="ACCESS_NOT_ASSIGNED", message="Worker belongs to a different company.", severity="CRITICAL")
            passed = False
            
        if not any(w.id == user.id for w in site.assigned_workers):
            context.add_reason(code="ACCESS_NOT_ASSIGNED", message="Worker is not assigned to this site.", severity="ERROR")
            passed = False
            
        context.record_trace("Assignment", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _check_worker_readiness(cls, context: AccessContext) -> bool:
        user = context.user
        passed = True
        
        if user.role == UserRole.WORKER:
            readiness = WorkerReadinessService.evaluate(user)
            if not readiness.get("ready", False):
                context.add_reason(code="ACCESS_WORKER_NOT_READY", message="Worker is missing required operational readiness criteria.", severity="ERROR")
                passed = False
                
        context.record_trace("Worker Readiness", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _check_gps(cls, context: AccessContext) -> bool:
        site = context.site
        passed = True
        
        if site.latitude is not None and site.longitude is not None:
            if context.gps_latitude is None or context.gps_longitude is None:
                context.add_reason(code="ACCESS_GPS_MISSING", message="GPS coordinates are required to check in.", severity="WARNING")
                passed = False
            else:
                def haversine(lat1, lon1, lat2, lon2):
                    R = 6371000
                    phi_1 = math.radians(lat1)
                    phi_2 = math.radians(lat2)
                    delta_phi = math.radians(lat2 - lat1)
                    delta_lambda = math.radians(lon2 - lon1)
                    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    return R * c
                
                distance = haversine(site.latitude, site.longitude, context.gps_latitude, context.gps_longitude)
                if distance > site.geofence_radius_meters:
                    context.add_reason(code="ACCESS_GPS_OUTSIDE_GEOFENCE", message=f"Outside geofence. Distance: {distance:.2f}m", severity="WARNING")
                    passed = False
                    
        context.record_trace("GPS Validation", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _check_duplicate_attendance(cls, context: AccessContext) -> bool:
        user = context.user
        passed = True
        
        existing = context.session.query(Attendance).filter(
            Attendance.user_id == user.id,
            Attendance.status == AttendanceStatus.CHECKED_IN
        ).first()
        
        if existing:
            context.add_reason(code="ACCESS_DUPLICATE_ATTENDANCE", message="User already has an active check-in.", severity="ERROR")
            passed = False
            
        context.record_trace("Duplicate Attendance", "PASS" if passed else "FAIL")
        return passed

    @classmethod
    def _build_decision(cls, context: AccessContext) -> AccessDecision:
        allowed = len(context.reasons) == 0
        return AccessDecision(
            allowed=allowed,
            reasons=context.reasons,
            evaluated_at=datetime.now(timezone.utc)
        )
