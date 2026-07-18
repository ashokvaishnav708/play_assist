"""Pydantic request/response models for user accounts and auth tokens."""

from pydantic import BaseModel
from uuid import UUID
from typing import Union, List
from datetime import datetime


class UserBase(BaseModel):
    """Fields common to every user representation."""

    first_name: str
    last_name: str
    email: str


class UserCreateRequest(UserBase):
    """Body of a signup request; password is hashed before it's persisted."""

    password: str
    is_admin: bool = False
    # favorite_movies: List[str]


class UserResponse(UserBase):
    """User as returned to API clients (never includes the password)."""

    id: UUID
    is_admin: bool
    created_at: datetime
    # favorite_movies: List[str]


class UserUpdateRequest(BaseModel):
    """Partial update to a user; all fields besides id are optional."""

    id: UUID
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    is_admin: Union[bool, None] = None
    created_at: Union[datetime, None] = None
    # favorite_movies: Union[List[str], None] = None


class UserLoginRequest(BaseModel):
    """Body of a login request."""

    email: str
    password: str


class TokenPair(BaseModel):
    """An access/refresh JWT pair returned by login and refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserWithToken(TokenPair):
    """Token pair plus the authenticated user, returned by login."""

    user: UserResponse


class RefreshRequest(BaseModel):
    """Body of a POST /auth/refresh request."""

    refresh_token: str
