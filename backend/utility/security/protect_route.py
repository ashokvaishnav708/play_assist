from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from typing import Annotated, Union
from .auth_handler import AuthHandler
from services.user_service import UserService
from db.database import get_db
from models.user import UserResponse

AUTH_PREFIX = 'Bearer '

def get_current_user(
        session: Session = Depends(get_db),
        authorization: Annotated[Union[str, None], Header()] = None
        ) -> UserResponse:

    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication.")

    if not authorization:
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    payload = AuthHandler.deode_jwt(token=authorization[len(AUTH_PREFIX):])

    if payload and payload.get("user_id"):
        try:
            user_id = UUID(payload["user_id"])
        except ValueError:
            raise auth_exception
        try:
            return UserService(session=session).get_user_by_id(user_id)
        except Exception as e:
            raise e
    raise auth_exception
            
    
