from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.models.models import User, UserRole, WorkerStatus

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user_allow_pending(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        session_id: str = payload.get("session_id")
        if user_id is None or session_id is None:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    
    from app.models.models import Session as AuthSession
    auth_session = db.query(AuthSession).filter(AuthSession.id == session_id).first()
    if not auth_session or auth_session.is_revoked:
        raise HTTPException(status_code=401, detail="Session revoked or invalid")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user(
    user: User = Depends(get_current_user_allow_pending)
) -> User:
    if user.status == WorkerStatus.PENDING:
        raise HTTPException(status_code=400, detail="Pending approval")
    if user.status != WorkerStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.SYSTEM_ADMIN:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

class RoleChecker:
    """
    DEPRECATED: Retained for backwards compatibility. Use PermissionChecker instead.
    """
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles and user.role != UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=403, detail="Operation not permitted"
            )
        return user

from app.services.authorization_service import AuthorizationService

class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(
        self,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if user.role != UserRole.SYSTEM_ADMIN:
            # Tenant-aware authorization
            get_current_tenant(current_user=user, db=db)
            
        permissions = AuthorizationService.resolve_permissions(db, user)
        if self.required_permission not in permissions:
            raise HTTPException(status_code=403, detail="Operation not permitted")
            
        return user

from app.models.models import Company

def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Company:
    if not current_user.company_id:
        raise HTTPException(status_code=403, detail="User is not associated with a tenant")
        
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    if not company:
        raise HTTPException(status_code=403, detail="Tenant context is invalid")
        
    return company
