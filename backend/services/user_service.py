from db.respository.user import UserRepository
from models.user import UserCreateRequest, UserLoginRequest, UserWithToken, UserResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from utility.security.hash_helper import HashHelper
from utility.security.auth_handler import AuthHandler

class UserService:
    def __init__(self, session: Session):
        self.__user_repo = UserRepository(session=session)

    def signup(self, user_data: UserCreateRequest) -> UserResponse:
        if self.__user_repo.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="User already exists, please login.")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_data.password)
        user_data.password = hashed_password

        user = self.__user_repo.create_user(user_data=user_data)

        return UserResponse(**user.__dict__)
    
    def login(self, login_details: UserLoginRequest) -> UserWithToken:
        if not self.__user_repo.get_user_by_email(login_details.email):
            raise HTTPException(status_code=400, detail="User does not exists, please signup to login.")
        
        user = self.__user_repo.get_user_by_email(email=login_details.email)

        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request.")
        raise HTTPException(status_code=400, detail="Please check your credentials.")
    
    def get_user_by_id(self, user_id: UUID) -> UserResponse:
        user = self.__user_repo.get_user_by_id(user_id=user_id)

        if user:
            return UserResponse(**user.__dict__)
        raise HTTPException(status_code=400, detail="User is not available.")
    
    def get_user(self) -> UserResponse:
        user = self.__user_repo.get_user()

        if user:
            return UserResponse(**user.__dict__)
        raise HTTPException(status_code=400, detail="User not found.")