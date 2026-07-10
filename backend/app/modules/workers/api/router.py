from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_current_tenant
from app.models.models import User, Company
from ..schemas.worker_dto import WorkerDetailResponse
from ..services.worker_service import WorkerService

router = APIRouter()

@router.get("/{id}", response_model=WorkerDetailResponse)
def get_worker_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_tenant: Company = Depends(get_current_tenant)
):
    service = WorkerService(db)
    # The tenant boundary is enforced by passing the tenant id to the service
    return service.get_worker_detail(worker_id=id, company_id=current_tenant.id)
