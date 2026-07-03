"""
ConstructPulse API — Application Entrypoint
==========================================
FastAPI application with enterprise-grade configuration:
  - Structured logging
  - Lifespan context manager (replaces deprecated @on_event)
  - CORS from settings
  - Rate limiting
  - OpenAPI metadata
  - Root endpoint
  - Health endpoint
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.api.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.db.database import Base, SessionLocal, engine
from app.middleware.request_context import RequestContextMiddleware

# ─── Logging ─────────────────────────────────────────────────────────────────
setup_logging()
logger = logging.getLogger("constructpulse.main")


# ─── Startup seeding ─────────────────────────────────────────────────────────

def _seed_demo_data(db: Session) -> None:
    """
    Insert minimal demo data on first boot if the records are absent.
    Only runs when the table is empty to avoid conflicting with migrations.
    Uses actual model field names (company_name, not name).
    """
    from app.models.models import Company, Contractor, Department

    company = (
        db.query(Company)
        .filter(Company.company_name == "Demo Company")
        .first()
    )
    if not company:
        company = Company(
            id="demo_company",
            company_name="Demo Company",
            registration_number="DEMO-001",
            contact_email="demo@constructpulse.com",
            contact_phone="1234567890",
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        logger.info("Demo company seeded | id=%s", company.id)

    if not db.query(Department).filter(Department.id == "d3").first():
        db.add(
            Department(
                id="d3",
                company_id=company.id,
                name="Electrical",
                description="Demo Department",
            )
        )
        logger.info("Demo department seeded | id=d3")

    if not db.query(Contractor).filter(Contractor.id == "c1").first():
        db.add(
            Contractor(
                id="c1",
                company_id=company.id,
                name="Demo Contractor",
                phone="9999999999",
                trade="Electrical",
            )
        )
        logger.info("Demo contractor seeded | id=c1")

    db.commit()


# ─── Lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifecycle manager.
    Handles startup and shutdown events.
    Replaces deprecated @app.on_event decorator.
    """
    # ── Startup ──────────────────────────────────────────────────────────────
    logger.info(
        "ConstructPulse starting | environment=%s | version=%s",
        settings.ENVIRONMENT,
        settings.VERSION,
    )

    db: Session = SessionLocal()
    try:
        _seed_demo_data(db)
    except OperationalError as exc:
        # Tables may not exist yet (migration needed) — log and continue
        logger.warning(
            "Demo seeding skipped — database tables not ready: %s", exc
        )
    except Exception as exc:
        logger.error("Demo seeding failed unexpectedly: %s", exc, exc_info=True)
    finally:
        db.close()

    logger.info("ConstructPulse startup complete")
    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    logger.info("ConstructPulse shutting down")


# ─── Application factory ─────────────────────────────────────────────────────

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    contact={
        "name": "ConstructPulse Engineering",
        "email": "engineering@constructpulse.com",
    },
    license_info={
        "name": "Proprietary",
    },
    lifespan=lifespan,
)

# ─── Rate limiting ────────────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ─── Exception handlers ───────────────────────────────────────────────────────

setup_exception_handlers(app)

# ─── Middleware ───────────────────────────────────────────────────────────────

app.add_middleware(RequestContextMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────

app.include_router(api_router, prefix=settings.API_V1_STR)

# ─── Core endpoints ───────────────────────────────────────────────────────────


@app.get("/", tags=["platform"], summary="Root")
def root() -> JSONResponse:
    """Platform root — confirms the API is reachable."""
    return JSONResponse(
        content={
            "application": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "status": "online",
            "docs": f"{settings.API_V1_STR}/docs",
        }
    )


@app.get("/health", tags=["platform"], summary="Health Check")
def health() -> JSONResponse:
    """
    Liveness probe endpoint.
    Returns HTTP 200 when the application is running.
    Used by Docker health checks, load balancers, and monitoring systems.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


@app.get("/version", tags=["platform"], summary="Version Info")
def version() -> JSONResponse:
    """Returns application version information."""
    return JSONResponse(
        content={
            "version": settings.VERSION,
            "api_version": settings.API_V1_STR,
            "environment": settings.ENVIRONMENT,
        }
    )
