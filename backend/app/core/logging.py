"""
ConstructPulse — Enterprise Logging Configuration
Provides structured, leveled logging for production use.
"""

import logging
import sys
from app.core.config import settings


def setup_logging() -> None:
    """Configure application-wide logging based on environment settings."""

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Root logger
    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Quieten noisy third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("firebase_admin").setLevel(logging.WARNING)

    logger = logging.getLogger("constructpulse")
    logger.info(
        "Logging initialised | environment=%s | level=%s",
        settings.ENVIRONMENT,
        settings.LOG_LEVEL,
    )


def get_logger(name: str = "constructpulse.application") -> logging.Logger:
    """Get a standard application logger."""
    return logging.getLogger(name)


def get_audit_logger() -> logging.Logger:
    """Get the dedicated audit logger for business events."""
    return logging.getLogger("constructpulse.audit")
