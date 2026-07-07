import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── Project metadata ──────────────────────────────────────────────────────
    PROJECT_NAME: str = "ConstructPulse API"
    DESCRIPTION: str = (
        "ConstructPulse — Construction Workforce Operating System. "
        "Enterprise-grade workforce management, attendance, compliance, and safety platform."
    )
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api/v1"

    # ── Runtime environment ───────────────────────────────────────────────────
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    FIREBASE_SERVICE_ACCOUNT_PATH: str | None = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/constructpulse",
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://constructpulse.com",
    ]

    # ── Feature flags ─────────────────────────────────────────────────────────
    DEMO_AUTH: bool = False
    
    # ── Secure Token Engine ───────────────────────────────────────────────────
    SECURE_TOKEN_LIFETIME_SECONDS: int = int(os.getenv("SECURE_TOKEN_LIFETIME_SECONDS", "60"))
    SECURE_TOKEN_GRACE_SECONDS: int = int(os.getenv("SECURE_TOKEN_GRACE_SECONDS", "5"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
