from fastapi import APIRouter
from app.api.endpoints import auth, companies, departments, contractors, users, sites, attendance, occupancy, public

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(contractors.router, prefix="/contractors", tags=["contractors"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(occupancy.router, prefix="/occupancy", tags=["occupancy"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
