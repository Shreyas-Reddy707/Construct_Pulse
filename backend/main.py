from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.api import api_router
from app.core.config import settings
from app.db.database import engine, Base

# In a real environment, use Alembic for migrations instead of create_all
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://constructpulse.com"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import Company, Department, Contractor

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    db: Session = SessionLocal()
    try:
        # Check if demo data needs to be seeded
        company = db.query(Company).filter(Company.name == "Demo Company").first()
        if not company:
            company = Company(
                id="demo_company",
                name="Demo Company",
                address="123 Builder Lane",
                phone="1234567890"
            )
            db.add(company)
            db.commit()
            db.refresh(company)

        department = db.query(Department).filter(Department.id == "d3").first()
        if not department:
            department = Department(
                id="d3",
                company_id=company.id,
                name="Electrical",
                description="Demo Department"
            )
            db.add(department)

        contractor = db.query(Contractor).filter(Contractor.id == "c1").first()
        if not contractor:
            contractor = Contractor(
                id="c1",
                company_id=company.id,
                name="Demo Contractor",
                phone="9999999999",
                trade="Electrical"
            )
            db.add(contractor)
        
        db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to ConstructPulse API"}
