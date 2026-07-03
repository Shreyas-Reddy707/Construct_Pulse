from sqlalchemy.orm import Session
from app.models.models import User, Role

class AuthorizationService:
    """
    AuthorizationService resolves permissions for a given user from the database.
    It follows the RBAC schema: Role -> Permission Group -> Permission.
    """
    @staticmethod
    def resolve_permissions(db: Session, user: User) -> set[str]:
        if not user or not user.role:
            return set()
            
        role_name = user.role.value if hasattr(user.role, "value") else user.role
        role = db.query(Role).filter(Role.name == role_name).first()
        
        if not role:
            return set()
            
        permissions = set()
        for group in role.permission_groups:
            for permission in group.permissions:
                permissions.add(permission.name)
                
        return permissions
