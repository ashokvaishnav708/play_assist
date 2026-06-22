from fastapi import APIRouter, Depends
from models.user import UserCreateRequest, UserLoginRequest, UserWithToken, UserResponse
from db.database import get_db
from sqlalchemy.orm import Session
from services.user_service import UserService

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