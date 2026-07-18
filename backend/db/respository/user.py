"""Data-access layer for the users table."""

from .base import BaseRepository
from db.schema import User
from models.user import UserCreateRequest
from uuid import UUID


class UserRepository(BaseRepository):
    """CRUD and query operations for User rows."""

    def create_user(self, user_data: UserCreateRequest):
        """Insert a new user row; raises if a user with the same email already exists."""
        new_user = User(**user_data.model_dump(exclude_none=True))

        if self.user_exist_by_email(user_data.email):
            raise Exception("User already exists. Skipping...")

        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        return new_user

    def user_exist_by_email(self, email: str) -> bool:
        """Return True if a user with the given email already exists."""
        user = self._session.query(User).filter_by(email=email).first()
        return bool(user)

    def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by email, or None if not found."""
        user = self._session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, id: UUID) -> User | None:
        """Fetch a user by their internal UUID, or None if not found."""
        user = self._session.query(User).filter_by(id=id).first()
        return user

    def get_user(self) -> User | None:
        """Fetch an arbitrary (first) user row. Used by admin/debug flows."""
        user = self._session.query(User).first()
        return user

    def increment_token_version(self, user_id: UUID) -> User | None:
        """Bump the user's token_version, invalidating all previously issued JWTs."""
        user = self.get_user_by_id(user_id)
        if user:
            user.token_version += 1
            self._session.commit()
            self._session.refresh(user)
        return user