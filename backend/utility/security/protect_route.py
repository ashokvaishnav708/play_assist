"""FastAPI dependency that guards routes behind a valid bearer JWT."""

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from typing import Annotated, Union
from .auth_handler import AuthHandler, TokenExpiredError, TokenInvalidError
from services.user_service import UserService
from db.database import get_db
from models.user import UserResponse

AUTH_PREFIX = 'Bearer '

def get_current_user(
        session: Session = Depends(get_db),
        authorization: Annotated[Union[str, None], Header()] = None
        ) -> UserResponse:
    """FastAPI dependency that resolves the current user from the `Authorization` header.

    Use via `Depends(get_current_user)` on any route that must be authenticated.
    Raises HTTPException(401) for a missing/malformed header, an expired or
    invalid token, a refresh token used as an access token, or a token whose
    version no longer matches the user's current one.
    """

    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication.")

    if not authorization or not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    try:
        payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])
    except TokenExpiredError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
    except TokenInvalidError:
        raise auth_exception

    # a refresh token must never be accepted as an access token
    if payload.get("refresh") or not payload.get("user_id"):
        raise auth_exception

    try:
        user_id = UUID(payload["user_id"])
    except ValueError:
        raise auth_exception

    return UserService(session=session).get_current_user(user_id=user_id, token_version=payload.get("token_version"))
