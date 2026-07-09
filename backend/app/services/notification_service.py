from typing import List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, Sequence, and_

from app.models.models import (
    Notification, NotificationRecipient, NotificationAuditLog,
    NotificationType, NotificationPriority, RecipientStatus, NotificationSource,
    User, UserRole
)
from app.schemas.schemas import (
    NotificationCreate, NotificationResponse, NotificationRecipientResponse,
    NotificationDashboard, NotificationSummary
)

class NotificationService:
    """
    Public Service Contract:
    NotificationService is the exclusive public interface for Notification Foundation.
    Future domains must consume NotificationService.
    They must never query Notification tables directly.
    
    Architectural Documentation:
    Notification is an immutable aggregate.
    Recipient lifecycle is fully owned by NotificationRecipient.
    NotificationRecipient state transitions never mutate Notification.
    """

    @classmethod
    def _generate_notification_number(cls, db: Session) -> str:
        # Sequence generation is database-driven to ensure atomic, gapless sequence numbers under concurrent load.
        year = datetime.now(timezone.utc).year
        seq_val = db.execute(Sequence('notification_number_seq')).scalar()
        return f"NOT-{year}-{seq_val:06d}"

    @classmethod
    def _map_recipient_to_dto(cls, recipient: NotificationRecipient) -> NotificationRecipientResponse:
        return NotificationRecipientResponse(
            id=recipient.id,
            user_id=recipient.user_id,
            recipient_status=recipient.recipient_status,
            read_at=recipient.read_at,
            archived_at=recipient.archived_at
        )

    @classmethod
    def _map_notification_to_dto(cls, notification: Notification) -> NotificationResponse:
        return NotificationResponse(
            id=notification.id,
            company_id=notification.company_id,
            site_id=notification.site_id,
            notification_number=notification.notification_number,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            priority=notification.priority,
            notification_source=notification.notification_source,
            notification_version=notification.notification_version,
            created_by=notification.created_by,
            created_at=notification.created_at,
            recipients=[cls._map_recipient_to_dto(r) for r in notification.recipients]
        )

    @classmethod
    def _create_audit_log(cls, db: Session, notification_id: str, notification_version: int, audit_batch_id: str, old_status: Optional[RecipientStatus], new_status: Optional[RecipientStatus], performed_by: str, reason: str):
        # Audit Documentation: NotificationAuditLog captures recipient lifecycle transition, 
        # notification_version snapshot, audit_batch_id, performed_by, and performed_at.
        # It does NOT represent mutations of the Notification aggregate.
        audit = NotificationAuditLog(
            notification_id=notification_id,
            notification_version=notification_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=new_status,
            performed_by=performed_by,
            reason=reason
        )
        db.add(audit)

    @classmethod
    def resolve_recipients(cls, db: Session, company_id: str, payload: NotificationCreate) -> List[str]:
        target_user_ids = set()

        if payload.target_user_ids:
            # Validate user IDs
            users = db.query(User).filter(User.id.in_(payload.target_user_ids), User.company_id == company_id).all()
            for u in users:
                target_user_ids.add(u.id)

        if payload.target_role:
            # Resolve by role
            role_users = db.query(User).filter(User.company_id == company_id, User.role == payload.target_role).all()
            for u in role_users:
                target_user_ids.add(u.id)

        return list(target_user_ids)

    @classmethod
    def create_notification(cls, db: Session, company_id: str, current_user_id: str, payload: NotificationCreate) -> NotificationResponse:
        from app.core.exceptions import ValidationException, ResourceNotFoundException, StateTransitionException, TenantIsolationException
        if not company_id:
            raise TenantIsolationException("User must belong to a company")
        # Validate targets
        recipient_ids = cls.resolve_recipients(db, company_id, payload)
        from app.core.exceptions import ValidationException, ResourceNotFoundException, StateTransitionException
        if not recipient_ids:
            raise ValidationException("No valid recipients resolved for notification")

        notification_number = cls._generate_notification_number(db)

        # Create root aggregate
        notification = Notification(
            company_id=company_id,
            site_id=payload.site_id,
            notification_number=notification_number,
            title=payload.title,
            message=payload.message,
            notification_type=payload.notification_type,
            priority=payload.priority,
            notification_source=NotificationSource.API,
            created_by=current_user_id
        )
        db.add(notification)
        db.flush()

        audit_batch_id = str(uuid.uuid4())

        # Create child entities
        for user_id in recipient_ids:
            recipient = NotificationRecipient(
                notification_id=notification.id,
                user_id=user_id,
                recipient_status=RecipientStatus.UNREAD
            )
            db.add(recipient)

        # Append audit log
        cls._create_audit_log(
            db=db,
            notification_id=notification.id,
            notification_version=notification.notification_version,
            audit_batch_id=audit_batch_id,
            old_status=None,
            new_status=RecipientStatus.UNREAD,
            performed_by=current_user_id,
            reason=f"Notification created for {len(recipient_ids)} recipient(s)"
        )

        db.commit()
        db.refresh(notification)
        return cls._map_notification_to_dto(notification)

    @classmethod
    def mark_read(cls, db: Session, notification_id: str, current_user_id: str, reason: Optional[str] = None) -> NotificationResponse:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not notification:
            raise ResourceNotFoundException("Notification not found")

        recipient = db.query(NotificationRecipient).filter(
            NotificationRecipient.notification_id == notification_id,
            NotificationRecipient.user_id == current_user_id
        ).first()

        if not recipient:
            raise ResourceNotFoundException("Recipient record not found for this user")

        if recipient.recipient_status != RecipientStatus.UNREAD:
            raise StateTransitionException("Only UNREAD notifications can be marked READ")

        # Lifecycle Documentation: UNREAD -> READ
        # This lifecycle belongs exclusively to NotificationRecipient.
        # Update ONLY NotificationRecipient
        old_status = recipient.recipient_status
        recipient.recipient_status = RecipientStatus.READ
        recipient.read_at = datetime.now(timezone.utc)

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            notification_id=notification.id,
            notification_version=notification.notification_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=recipient.recipient_status,
            performed_by=current_user_id,
            reason=reason or "Marked as read"
        )

        db.commit()
        db.refresh(notification)
        return cls._map_notification_to_dto(notification)

    @classmethod
    def archive(cls, db: Session, notification_id: str, current_user_id: str, reason: Optional[str] = None) -> NotificationResponse:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        from app.core.exceptions import ResourceNotFoundException, StateTransitionException
        if not notification:
            raise ResourceNotFoundException("Notification not found")

        recipient = db.query(NotificationRecipient).filter(
            NotificationRecipient.notification_id == notification_id,
            NotificationRecipient.user_id == current_user_id
        ).first()

        if not recipient:
            raise ResourceNotFoundException("Recipient record not found for this user")

        if recipient.recipient_status == RecipientStatus.ARCHIVED:
            raise StateTransitionException("Notification is already ARCHIVED")

        # Lifecycle Documentation: READ -> ARCHIVED (or UNREAD -> ARCHIVED)
        # This lifecycle belongs exclusively to NotificationRecipient.
        # Update ONLY NotificationRecipient
        old_status = recipient.recipient_status
        recipient.recipient_status = RecipientStatus.ARCHIVED
        recipient.archived_at = datetime.now(timezone.utc)

        audit_batch_id = str(uuid.uuid4())
        cls._create_audit_log(
            db=db,
            notification_id=notification.id,
            notification_version=notification.notification_version,
            audit_batch_id=audit_batch_id,
            old_status=old_status,
            new_status=recipient.recipient_status,
            performed_by=current_user_id,
            reason=reason or "Archived"
        )

        db.commit()
        db.refresh(notification)
        return cls._map_notification_to_dto(notification)

    @classmethod
    def get_notification(cls, db: Session, notification_id: str, current_user_id: str) -> Optional[NotificationResponse]:
        # User must be a recipient
        recipient = db.query(NotificationRecipient).filter(
            NotificationRecipient.notification_id == notification_id,
            NotificationRecipient.user_id == current_user_id
        ).first()

        if not recipient:
            return None

        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            return cls._map_notification_to_dto(notification)
        return None

    @classmethod
    def list_notifications(cls, db: Session, current_user_id: str, skip: int = 0, limit: int = 100) -> List[NotificationResponse]:
        # Query notifications where the user is a recipient
        notifications = db.query(Notification).join(NotificationRecipient).filter(
            NotificationRecipient.user_id == current_user_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return [cls._map_notification_to_dto(n) for n in notifications]

    @classmethod
    def dashboard(cls, db: Session, current_user_id: str) -> NotificationDashboard:
        # Dashboard is recipient-centric, providing counts for the current user
        counts = db.query(
            NotificationRecipient.recipient_status, 
            func.count(NotificationRecipient.id)
        ).filter(
            NotificationRecipient.user_id == current_user_id
        ).group_by(NotificationRecipient.recipient_status).all()

        counts_dict = {status: count for status, count in counts}

        summary = NotificationSummary(
            unread=counts_dict.get(RecipientStatus.UNREAD, 0),
            read=counts_dict.get(RecipientStatus.READ, 0),
            archived=counts_dict.get(RecipientStatus.ARCHIVED, 0)
        )

        return NotificationDashboard(
            report_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            summary=summary
        )
