from sqlalchemy.orm import Session
from app.models.models import User, WorkerStatus
from typing import List, Dict

class WorkerReadinessService:
    
    @classmethod
    def evaluate(cls, worker: User) -> dict:
        """
        Evaluate if a worker is operationally ready to be deployed.
        Aggregates requirements from identity, assignment, safety, and compliance.
        """
        missing_requirements = cls.missing_requirements(worker)
        return {
            "ready": len(missing_requirements) == 0,
            "missing": missing_requirements
        }

    @classmethod
    def is_ready(cls, worker: User) -> bool:
        """
        Quick check to determine if worker is completely ready.
        """
        return len(cls.missing_requirements(worker)) == 0

    @classmethod
    def missing_requirements(cls, worker: User) -> List[Dict[str, str]]:
        """
        Returns a structured list of unmet requirements for operational readiness.
        """
        missing = []
        missing.extend(cls._check_identity(worker))
        missing.extend(cls._check_assignment(worker))
        missing.extend(cls._check_safety(worker))
        missing.extend(cls._check_compliance(worker))
        return missing

    @classmethod
    def evaluate_worker_readiness(cls, worker: User) -> dict:
        """
        Alias for evaluate to maintain compatibility with existing endpoint.
        """
        return cls.evaluate(worker)

    @classmethod
    def _check_identity(cls, worker: User) -> List[Dict[str, str]]:
        missing = []
        if worker.status != WorkerStatus.APPROVED:
            missing.append({
                "code": "IDENTITY_NOT_APPROVED",
                "message": "Worker status must be APPROVED."
            })
            
        if not worker.is_active:
            missing.append({
                "code": "IDENTITY_INACTIVE",
                "message": "Worker account is inactive."
            })

        if not worker.designation:
            missing.append({
                "code": "IDENTITY_MISSING_DESIGNATION",
                "message": "Worker must have a defined trade or designation."
            })

        if not worker.emergency_contact_name or not worker.emergency_contact_phone:
            missing.append({
                "code": "IDENTITY_MISSING_EMERGENCY_CONTACT",
                "message": "Worker must provide emergency contact information."
            })
        return missing

    @classmethod
    def _check_assignment(cls, worker: User) -> List[Dict[str, str]]:
        missing = []
        if not worker.company_id and not worker.contractor_id:
            missing.append({
                "code": "ASSIGNMENT_MISSING_EMPLOYER",
                "message": "Worker must be assigned to an Employer (Company or Contractor)."
            })

        has_active_site = any(site.status == "active" for site in worker.assigned_sites)
        if not has_active_site:
            missing.append({
                "code": "ASSIGNMENT_MISSING_SITE",
                "message": "Worker must be assigned to at least one active site."
            })
        return missing

    @classmethod
    def _check_safety(cls, worker: User) -> List[Dict[str, str]]:
        # Returns PASS for now (Batch 1B Constraint)
        return []

    @classmethod
    def _check_compliance(cls, worker: User) -> List[Dict[str, str]]:
        # Returns PASS for now (Batch 1B Constraint)
        return []
