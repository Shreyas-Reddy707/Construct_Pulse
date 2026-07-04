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
        Atomically publishes a new token generation for the given site.
        This handles:
        1. Locking the site's token generation to prevent race conditions.
        2. Generating a secure opaque token.
        3. Deactivating the previous generation.
        4. Activating the new generation.
        """
        now_utc = datetime.now(timezone.utc)
        lifetime = lifetime_seconds if lifetime_seconds is not None else settings.SECURE_TOKEN_LIFETIME_SECONDS
        
        # Concurrency Safety: Lock the latest generation record using with_for_update()
        # This prevents duplicate generations if multiple admins publish simultaneously.
        max_gen_record = session.query(SiteQRCode).filter(
            SiteQRCode.site_id == site.id
        ).order_by(
            SiteQRCode.generation.desc()
        ).with_for_update().first()
        
        latest_generation = max_gen_record.generation if max_gen_record else 0
        new_generation = latest_generation + 1

        # Deactivate all previously active tokens for this site
        active_tokens = session.query(SiteQRCode).filter(
            SiteQRCode.site_id == site.id,
            SiteQRCode.is_active == True
        ).all()
        
        for token in active_tokens:
            token.is_active = False
            if token.expires_at and token.expires_at.replace(tzinfo=timezone.utc) > now_utc:
                # Force early expiration
                token.expires_at = now_utc

        # Cryptographically secure, unpredictable, and opaque token
        new_token_str = secrets.token_urlsafe(32)
        
        new_qr = SiteQRCode(
            site_id=site.id,
            qr_token=new_token_str,
            generation=new_generation,
            issued_at=now_utc,
            expires_at=now_utc + timedelta(seconds=lifetime),
            is_active=True,
            created_by=created_by
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
        Calling this rotates the current active token to a new generation.
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
    def validate_token(cls, session: Session, token: str) -> str:
        """
        Validates the token, cleanly distinguishing between REVOKED, EXPIRED, INVALID, and VALID.
        Includes support for the SECURE_TOKEN_GRACE_SECONDS configuration.
        """
        qr = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if not qr:
            return "INVALID"
            
        if qr.revoked_at is not None:
            return "REVOKED"
            
        now_utc = datetime.now(timezone.utc)
        expires_at = qr.expires_at.replace(tzinfo=timezone.utc) if qr.expires_at.tzinfo is None else qr.expires_at
        
        # Consider the grace window for expiration
        if expires_at + timedelta(seconds=settings.SECURE_TOKEN_GRACE_SECONDS) < now_utc:
            return "EXPIRED"
            
        # Even if is_active is False (e.g. it was just rotated), we allow it if it is within the grace window
        return "VALID"

    @classmethod
    def expire_token(cls, session: Session, token: str) -> bool:
        """
        Forces a token to immediately expire without revoking it.
        """
        qr = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if not qr:
            return False
            
        now_utc = datetime.now(timezone.utc)
        qr.expires_at = now_utc
        qr.is_active = False
        session.commit()
        return True

    @classmethod
    def revoke_token(cls, session: Session, token: str) -> bool:
        """
        Immediately and permanently revokes a token (e.g. for administrative reasons).
        Revoked tokens bypass the grace window.
        """
        qr = session.query(SiteQRCode).filter(SiteQRCode.qr_token == token).first()
        if not qr:
            return False
            
        now_utc = datetime.now(timezone.utc)
        qr.revoked_at = now_utc
        qr.is_active = False
        qr.expires_at = now_utc
        session.commit()
        return True
