from fastapi import APIRouter, Depends
from models.user import UserCreateRequest, UserLoginRequest, UserWithToken, UserResponse, TokenPair, RefreshRequest
from db.database import get_db
from sqlalchemy.orm import Session
from services.user_service import UserService
from utility.security.protect_route import get_current_user

from logging import getLogger

logger = getLogger(__name__)

router = APIRouter()


@router.post("/login", status_code=200, response_model=UserWithToken)
def login(user_login: UserLoginRequest, session: Session = Depends(get_db)):
    try:
        return UserService(session).login(login_details=user_login)
    except Exception as e:
        logger.error(f"Error loggin in: {e}")
        raise e

@router.post("/signup", status_code=200, response_model=UserResponse)
def sign_up(user_data: UserCreateRequest, session: Session = Depends(get_db)):
    try:
        return UserService(session).signup(user_data=user_data)
    except Exception as e:
        logger.error(f"Error signing up user: {e}")
        raise e

@router.post("/refresh", status_code=200, response_model=TokenPair)
def refresh(refresh_request: RefreshRequest, session: Session = Depends(get_db)):
    try:
        return UserService(session).refresh(refresh_token=refresh_request.refresh_token)
    except Exception as e:
        logger.error(f"Error refreshing token: {e}")
        raise e

@router.post("/logout", status_code=200)
def logout(current_user: UserResponse = Depends(get_current_user), session: Session = Depends(get_db)):
    try:
        UserService(session).logout(user_id=current_user.id)
        return {"detail": "Logged out successfully."}
    except Exception as e:
        logger.error(f"Error logging out: {e}")
        raise e

@router.get("/me", status_code=200, response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
