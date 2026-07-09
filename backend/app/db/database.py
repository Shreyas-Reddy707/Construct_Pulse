from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from app.db.uow import UnitOfWork

def get_db():
    """
    Dependency for managing database sessions across the request lifecycle.
    
    This function acts as the centralized owner of the request transaction:
    - Starts the transaction (implicitly on session access).
    - Automatically rolls back if an exception occurs during the request.
    - Guarantees session cleanup upon completion.
    
    Note: Temporary backwards compatibility is maintained by yielding the
    raw SQLAlchemy session. Explicit commit() ownership currently remains
    within individual services until migration in WS1-P3B.
    """
    with UnitOfWork() as uow:
        yield uow.session
