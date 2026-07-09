from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.models.models import Site, SiteQRCode

class SecureTokenService:
    """
    Secure Token Engine responsible for generating, rotating, validating, 
    resolving, revoking, and expiring secure temporary access tokens.
    Remains completely independent of presentation mechanisms (QR, NFC, etc.) 
    and contains no attendance or worker authorization logic.
    """
    
    @classmethod
    def publish_generation(
        cls, 
        session: Session, 
        site: Site, 
        created_by: Optional[str] = None,
        lifetime_seconds: Optional[int] = None
    ) -> SiteQRCode:
        """
        Atomically publishes a new token for the given site.
        Expires all previously generated active tokens for this site.
        """
        now_utc = datetime.now(timezone.utc)
        lifetime = lifetime_seconds if lifetime_seconds is not None else settings.SECURE_TOKEN_LIFETIME_SECONDS
        
        # Concurrency Safety: Lock the latest record to prevent concurrent duplicate generations
        session.query(SiteQRCode).filter(
            SiteQRCode.site_id == site.id
        ).with_for_update().first()
        
        # Force early expiration of all unexpired tokens for this site
        active_tokens = session.query(SiteQRCode).filter(
            SiteQRCode.site_id == site.id,
            SiteQRCode.expires_at > now_utc
        ).all()
        
        for token in active_tokens:
            token.expires_at = now_utc

        # Cryptographically secure, unpredictable, and opaque token
        new_token_str = secrets.token_urlsafe(32)
        
        new_qr = SiteQRCode(
            site_id=site.id,
            qr_token=new_token_str,
            expires_at=now_utc + timedelta(seconds=lifetime)
        )
        
        session.add(new_qr)
        session.commit()
        session.refresh(new_qr)
        return new_qr

    @classmethod
    def generate_token(
        cls, 
        session: Session, 
        site: Site, 
        created_by: Optional[str] = None,
        lifetime_seconds: Optional[int] = None
    ) -> SiteQRCode:
        """
        Compatibility wrapper for publish_generation.
        Generates a new active, secure, opaque token for the given site.
        """
        return cls.publish_generation(session, site, created_by, lifetime_seconds)

    @classmethod
    def rotate_token(
        cls, 
        session: Session, 
        site: Site, 
        created_by: Optional[str] = None
    ) -> SiteQRCode:
        """
        Compatibility wrapper for publish_generation. 
        Calling this rotates the current active token to a new one.
        """
        return cls.publish_generation(session, site, created_by)

    @classmethod
    def resolve_site(cls, session: Session, token: str) -> Optional[Site]:
        """
        Resolves the Site associated with the given opaque token.
        Requires a single indexed lookup.
        """
        qr_record = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if qr_record:
            return qr_record.site
        return None

    @classmethod
    def validate_token(cls, session: Session, token: str) -> Site:
        """
        Validates the token.
        Includes support for the SECURE_TOKEN_GRACE_SECONDS configuration.
        Raises DomainException on failure.
        """
        from app.core.exceptions import ValidationException, ResourceNotFoundException
        from app.models.models import SiteStatus
        
        qr = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if not qr:
            raise ValidationException("Registration token is invalid.")
            
        now_utc = datetime.now(timezone.utc)
        
        if qr.expires_at:
            expires_at = qr.expires_at.replace(tzinfo=timezone.utc) if qr.expires_at.tzinfo is None else qr.expires_at
            # Consider the grace window for expiration
            if expires_at + timedelta(seconds=settings.SECURE_TOKEN_GRACE_SECONDS) < now_utc:
                raise ValidationException("Registration token has expired.")
            
        site = qr.site
        if not site:
            raise ResourceNotFoundException("Site could not be resolved from token.")
            
        if site.is_deleted or site.status != SiteStatus.ACTIVE.value:
            raise ValidationException("Site is no longer active.")
            
        if site.company and site.company.is_deleted:
            raise ValidationException("Company is no longer active.")
            
        return site

    @classmethod
    def expire_token(cls, session: Session, token: str) -> bool:
        """
        Forces a token to immediately expire.
        """
        qr = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if not qr:
            return False
            
        now_utc = datetime.now(timezone.utc)
        qr.expires_at = now_utc
        session.commit()
        return True

    @classmethod
    def revoke_token(cls, session: Session, token: str) -> bool:
        """
        Immediately and permanently revokes a token (e.g. for administrative reasons).
        Revocation is achieved by forcing expiration.
        """
        return cls.expire_token(session, token)
