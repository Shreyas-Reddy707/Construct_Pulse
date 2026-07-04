from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence, and_

from app.models.models import (
    PlatformConfiguration, ConfigurationVersion, ConfigurationAuditLog,
    ConfigCategory, ConfigurationStatus, ConfigurationSource
)
from app.schemas.schemas import (
    ConfigurationDraftRequest, ConfigurationApproveRequest, ConfigurationResponse,
    ConfigurationVersionResponse, ConfigurationDashboard, ConfigurationSummary
)

class PlatformConfigurationService:
    """
    Public Service Contract:
    PlatformConfigurationService is the exclusive public interface for the Platform Configuration Foundation.
    Future domains MUST consume this service.
    Future domains MUST NEVER directly query PlatformConfiguration or ConfigurationVersion ORM models.
    
    Platform Configuration is a provider domain.
    It exposes configuration but never consumes operational business domains.
    This guarantees a strictly downstream dependency flow.
    Downstream domains consume ONLY public service methods.

    Configuration Ownership Boundaries:
    - PlatformConfiguration (Root Aggregate) owns: metadata, company/site ownership, configuration key, category, and identity.
    - ConfigurationVersion owns: actual configuration values, version lifecycle, approval state, immutable snapshot, and historical record.
    The value itself does not belong on the root aggregate because operational changes must be version-controlled and auditable without mutating the aggregate's identity.

    Version Lifecycle:
    Configuration
        ↓
    Version 1
        ↓
    Version 2
        ↓
    Version 3
    
    - versions are append-only
    - versions are never overwritten
    - updating a configuration always creates a brand-new version
    - ACTIVE and ARCHIVED versions remain immutable forever
    """

    @classmethod
    def _generate_config_number(cls, db: Session) -> str:
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('configuration_number_seq')).scalar()
        return f"CFG-{year}-{seq_val:06d}"

    @classmethod
    def _create_audit_log(
        cls, db: Session, version_id: str, version_number: int, source: ConfigurationSource,
        audit_batch_id: str, old_status: Optional[ConfigurationStatus], new_status: Optional[ConfigurationStatus],
        performed_by: str, reason: str
    ):
        # Architectural Comment: Audit logs strictly record draft creation, approval, and archival.
        # Read-only operations intentionally DO NOT create audit entries in order to avoid unnecessary audit growth.
        audit = ConfigurationAuditLog(
            configuration_version_id=version_id,
            version_number=version_number,
            configuration_source=source,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def _map_version_to_dto(cls, version: ConfigurationVersion) -> ConfigurationVersionResponse:
        # Architectural Comment: ConfigurationVersion represents the complete immutable configuration snapshot.
        # Once ACTIVE or ARCHIVED: values never change, approvals never change, and historical versions remain reproducible forever.
        # Future operational domains must always evaluate configuration using these immutable snapshots.
        return ConfigurationVersionResponse(
            id=version.id,
            configuration_id=version.configuration_id,
            version_number=version.version_number,
            config_value=version.config_value,
            status=version.status,
            created_by=version.created_by,
            approved_by=version.approved_by,
            created_at=version.created_at,
            approved_at=version.approved_at,
            archived_at=version.archived_at
        )

    @classmethod
    def _map_to_dto(cls, db: Session, config: PlatformConfiguration) -> ConfigurationResponse:
        active_version_orm = db.query(ConfigurationVersion).filter(
            ConfigurationVersion.configuration_id == config.id,
            ConfigurationVersion.status == ConfigurationStatus.ACTIVE
        ).first()
        
        active_version_dto = None
        if active_version_orm:
            active_version_dto = cls._map_version_to_dto(active_version_orm)

        return ConfigurationResponse(
            id=config.id,
            company_id=config.company_id,
            site_id=config.site_id,
            configuration_number=config.configuration_number,
            config_key=config.config_key,
            category=config.category,
            configuration_source=config.configuration_source,
            created_by=config.created_by,
            created_at=config.created_at,
            active_version=active_version_dto
        )

    @classmethod
    def create_draft(
        cls, db: Session, company_id: str, current_user_id: str, payload: ConfigurationDraftRequest
    ) -> ConfigurationResponse:
        
        # Check if configuration already exists
        query = db.query(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id,
            PlatformConfiguration.config_key == payload.config_key
        )
        if payload.site_id:
            query = query.filter(PlatformConfiguration.site_id == payload.site_id)
        else:
            query = query.filter(PlatformConfiguration.site_id.is_(None))
            
        config = query.first()
        
        if not config:
            config = PlatformConfiguration(
                company_id=company_id,
                site_id=payload.site_id,
                configuration_number=cls._generate_config_number(db),
                config_key=payload.config_key,
                category=payload.category,
                configuration_source=ConfigurationSource.MANUAL,
                created_by=current_user_id
            )
            db.add(config)
            db.flush()
            version_number = 1
        else:
            # Find max version number
            # Architectural Comment: version_number prepares the foundation for long-term configuration history.
            max_version = db.query(func.max(ConfigurationVersion.version_number)).filter(
                ConfigurationVersion.configuration_id == config.id
            ).scalar()
            version_number = (max_version or 0) + 1

        version = ConfigurationVersion(
            configuration_id=config.id,
            version_number=version_number,
            config_value=payload.config_value,
            status=ConfigurationStatus.DRAFT,
            created_by=current_user_id
        )
        db.add(version)
        db.flush()

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            version_id=version.id,
            version_number=version.version_number,
            source=config.configuration_source,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=ConfigurationStatus.DRAFT,
            performed_by=current_user_id,
            reason="Created draft configuration version"
        )
        
        db.commit()
        db.refresh(config)
        return cls._map_to_dto(db, config)

    @classmethod
    def approve(
        cls, db: Session, version_id: str, current_user_id: str, payload: ConfigurationApproveRequest
    ) -> ConfigurationResponse:
        
        draft_version = db.query(ConfigurationVersion).filter(ConfigurationVersion.id == version_id).first()
        if not draft_version:
            raise ValueError("Configuration version not found")
            
        if draft_version.status != ConfigurationStatus.DRAFT:
            raise ValueError("Only DRAFT versions can be approved")
            
        config = db.query(PlatformConfiguration).filter(PlatformConfiguration.id == draft_version.configuration_id).first()
        if not config:
            raise ValueError("Configuration not found")
            
        audit_batch_id = str(uuid.uuid4())
        
        # Archive current ACTIVE version if it exists
        active_version = db.query(ConfigurationVersion).filter(
            ConfigurationVersion.configuration_id == config.id,
            ConfigurationVersion.status == ConfigurationStatus.ACTIVE
        ).first()
        
        if active_version:
            old_status = active_version.status
            active_version.status = ConfigurationStatus.ARCHIVED
            active_version.archived_at = datetime.now(timezone.utc)
            
            cls._create_audit_log(
                db=db,
                version_id=active_version.id,
                version_number=active_version.version_number,
                source=config.configuration_source,
                audit_batch_id=audit_batch_id,
                old_status=old_status,
                new_status=ConfigurationStatus.ARCHIVED,
                performed_by=current_user_id,
                reason=f"Archived by approval of version {draft_version.version_number}"
            )
            
        # Activate the new DRAFT version
        draft_version.status = ConfigurationStatus.ACTIVE
        draft_version.approved_by = current_user_id
        draft_version.approved_at = datetime.now(timezone.utc)
        
        cls._create_audit_log(
            db=db,
            version_id=draft_version.id,
            version_number=draft_version.version_number,
            source=config.configuration_source,
            audit_batch_id=audit_batch_id,
            old_status=ConfigurationStatus.DRAFT,
            new_status=ConfigurationStatus.ACTIVE,
            performed_by=current_user_id,
            reason=payload.reason
        )
        
        db.commit()
        db.refresh(config)
        return cls._map_to_dto(db, config)

    @classmethod
    def list_configurations(cls, db: Session, company_id: str) -> List[ConfigurationResponse]:
        configs = db.query(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id
        ).all()
        return [cls._map_to_dto(db, c) for c in configs]

    @classmethod
    def get_configuration_history(cls, db: Session, company_id: str, config_key: str) -> List[ConfigurationVersionResponse]:
        versions = db.query(ConfigurationVersion).join(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id,
            PlatformConfiguration.config_key == config_key
        ).order_by(ConfigurationVersion.version_number.desc()).all()
        return [cls._map_version_to_dto(v) for v in versions]

    @classmethod
    def dashboard(cls, db: Session, company_id: str) -> ConfigurationDashboard:
        counts = db.query(
            ConfigurationVersion.status,
            func.count(ConfigurationVersion.id)
        ).join(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id
        ).group_by(ConfigurationVersion.status).all()
        
        counts_dict = {status: count for status, count in counts}
        
        summary = ConfigurationSummary(
            draft=counts_dict.get(ConfigurationStatus.DRAFT, 0),
            active=counts_dict.get(ConfigurationStatus.ACTIVE, 0),
            archived=counts_dict.get(ConfigurationStatus.ARCHIVED, 0)
        )
        
        return ConfigurationDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )

    @classmethod
    def get_active_configuration(cls, db: Session, company_id: str, config_key: str) -> Optional[dict]:
        """
        Public certified read contract for retrieving active configuration at the company level.
        """
        version = db.query(ConfigurationVersion).join(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id,
            PlatformConfiguration.config_key == config_key,
            PlatformConfiguration.site_id.is_(None),
            ConfigurationVersion.status == ConfigurationStatus.ACTIVE
        ).first()
        
        return version.config_value if version else None

    @classmethod
    def get_active_configuration_for_site(cls, db: Session, company_id: str, site_id: str, config_key: str) -> Optional[dict]:
        """
        Public certified read contract for retrieving active configuration at the site level,
        falling back to company-level if a site-specific configuration does not exist.
        
        Resolution Contract:
        Site Configuration
            ↓
        If found
            ↓
        Return Site Configuration
            ↓
        Otherwise
            ↓
        Company Configuration
            ↓
        Return Company Default
        """
        # Check site specific first
        version = db.query(ConfigurationVersion).join(PlatformConfiguration).filter(
            PlatformConfiguration.company_id == company_id,
            PlatformConfiguration.site_id == site_id,
            PlatformConfiguration.config_key == config_key,
            ConfigurationVersion.status == ConfigurationStatus.ACTIVE
        ).first()
        
        if version:
            return version.config_value
            
        # Fallback to company wide
        return cls.get_active_configuration(db, company_id, config_key)
