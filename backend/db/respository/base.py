"""Base class for repository implementations."""

from sqlalchemy.orm import Session


class BaseRepository:
    """Holds the SQLAlchemy session shared by all entity-specific repositories."""

    def __init__(self, session: Session):
        self._session = session