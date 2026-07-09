from typing import Any, Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

class UnitOfWork:
    """
    Unit of Work (UoW) infrastructure pattern.
    
    This class is the centralized owner of a database transaction.
    It encapsulates the SQLAlchemy Session and provides explicit
    methods to commit, rollback, and close the transaction.
    
    Future services will receive this UoW instead of directly
    managing SQLAlchemy sessions, ensuring atomic operations and
    strict transaction boundaries.
    """
    
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory
        self._session: Optional[Session] = None
        
    @property
    def session(self) -> Session:
        """
        Provides access to the active SQLAlchemy Session.
        Initializes the session lazily on first access.
        """
        if self._session is None:
            self._session = self.session_factory()
        return self._session

    def __enter__(self) -> "UnitOfWork":
        """Support for 'with UnitOfWork() as uow:' usage."""
        return self
        
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Automatically closes the session when exiting the context manager.
        If an exception was raised within the context, the transaction is
        automatically rolled back before closing.
        """
        if exc_type is not None:
            self.rollback()
        self.close()

    def commit(self) -> None:
        """Commits the current transaction."""
        if self._session:
            self._session.commit()
            
    def rollback(self) -> None:
        """Rolls back the current transaction."""
        if self._session:
            self._session.rollback()
            
    def close(self) -> None:
        """Closes the current session and releases connection resources."""
        if self._session:
            self._session.close()
            self._session = None
