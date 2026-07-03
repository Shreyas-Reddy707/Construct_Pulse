from sqlalchemy.orm import Session
from app.models.models import Site, InductionPackage

class SafetyService:
    @classmethod
    def publish_induction_package(
        cls,
        db: Session,
        site_id: str,
        title: str,
        expiry_days: int = 365,
        quiz_enabled: bool = False
    ) -> InductionPackage:
        """
        Publishes a new InductionPackage for a Site.
        Enforces the business invariant that each Site has AT MOST ONE active package.
        When a newer package is published, the previous active package is deactivated.
        """
        # Fetch the site
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise ValueError(f"Site {site_id} not found")

        # Deactivate any currently active packages for this site
        active_packages = db.query(InductionPackage).filter(
            InductionPackage.site_id == site_id,
            InductionPackage.is_active == True
        ).all()

        for pkg in active_packages:
            pkg.is_active = False

        # Determine the next version
        latest_package = db.query(InductionPackage).filter(
            InductionPackage.site_id == site_id
        ).order_by(InductionPackage.version.desc()).first()
        
        next_version = (latest_package.version + 1) if latest_package else 1

        # Create and activate the new package
        new_package = InductionPackage(
            site_id=site_id,
            version=next_version,
            title=title,
            is_active=True,
            expiry_days=expiry_days,
            quiz_enabled=quiz_enabled
        )
        
        db.add(new_package)
        db.commit()
        db.refresh(new_package)
        
        return new_package
