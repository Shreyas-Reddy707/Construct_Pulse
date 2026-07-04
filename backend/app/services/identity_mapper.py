from app.models.models import IdentityType, UserRole

class IdentityMapper:
    """
    Responsibility: Maps IdentityType (workflow domain) to UserRole (application domain).
    """
    _mapping = {
        IdentityType.WORKER: UserRole.WORKER,
        IdentityType.VISITOR: UserRole.VISITOR,
        IdentityType.CONTRACTOR_REPRESENTATIVE: UserRole.SUPERVISOR,  # or another appropriate role
        IdentityType.SITE_ENGINEER: UserRole.SITE_MANAGER,
        IdentityType.INSPECTOR: UserRole.SAFETY_OFFICER,
        IdentityType.VENDOR: UserRole.WORKER
    }

    @classmethod
    def get_role(cls, identity_type: IdentityType) -> UserRole:
        """
        Returns the corresponding UserRole for a given IdentityType.
        Defaults to WORKER if no mapping exists, though all should be mapped.
        """
        return cls._mapping.get(identity_type, UserRole.WORKER)
