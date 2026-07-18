"""Business logic for user accounts and authentication (signup, login, token
refresh/logout, and current-user resolution)."""

from db.respository.user import UserRepository
from models.user import UserCreateRequest, UserLoginRequest, UserWithToken, UserResponse, TokenPair
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from utility.security.hash_helper import HashHelper
from utility.security.auth_handler import AuthHandler, ACCESS_TOKEN_EXPIRY_SECONDS, TokenExpiredError, TokenInvalidError

class UserService:
    """User account and auth use cases, backed by UserRepository."""

    def __init__(self, session: Session):
        self.__user_repo = UserRepository(session=session)

    def signup(self, user_data: UserCreateRequest) -> UserResponse:
        """Create a new user, hashing the plaintext password before it's stored."""
        if self.__user_repo.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="User already exists, please login.")

        hashed_password = HashHelper.get_password_hash(plain_password=user_data.password)
        user_data.password = hashed_password

        user = self.__user_repo.create_user(user_data=user_data)

        return UserResponse(**user.__dict__)

    def login(self, login_details: UserLoginRequest) -> UserWithToken:
        """Verify credentials and issue a fresh access/refresh JWT pair."""
        user = self.__user_repo.get_user_by_email(email=login_details.email)
        if not user:
            raise HTTPException(status_code=400, detail="User does not exists, please signup to login.")

        if not HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            raise HTTPException(status_code=400, detail="Please check your credentials.")

        access_token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version)
        refresh_token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version, refresh=True)

        return UserWithToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRY_SECONDS,
            user=UserResponse(**user.__dict__),
        )

    def refresh(self, refresh_token: str) -> TokenPair:
        """Validate a refresh token and issue a new access/refresh token pair.

        Rejects tokens that are expired, malformed, not marked as a refresh
        token, or whose token_version no longer matches the user's current
        one (i.e. the user has since logged out).
        """
        auth_exception = HTTPException(status_code=401, detail="Invalid refresh token.")

        try:
            payload = AuthHandler.decode_jwt(refresh_token)
        except TokenExpiredError:
            raise HTTPException(status_code=401, detail="Refresh token expired, please log in again.")
        except TokenInvalidError:
            raise auth_exception

        if not payload.get("refresh"):
            raise auth_exception

        try:
            user_id = UUID(payload["user_id"])
        except (ValueError, KeyError):
            raise auth_exception

        user = self.__user_repo.get_user_by_id(user_id)
        if not user or user.token_version != payload.get("token_version"):
            raise auth_exception

        access_token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version)
        new_refresh_token = AuthHandler.sign_jwt(user_id=user.id, token_version=user.token_version, refresh=True)

        return TokenPair(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRY_SECONDS,
        )

    def logout(self, user_id: UUID) -> None:
        """Invalidate all previously issued tokens for this user by bumping token_version."""
        self.__user_repo.increment_token_version(user_id=user_id)

    def get_current_user(self, user_id: UUID, token_version: int | None) -> UserResponse:
        """Resolve the user for a decoded JWT payload, rejecting stale (logged-out) tokens."""
        user = self.__user_repo.get_user_by_id(user_id)
        if not user or user.token_version != token_version:
            raise HTTPException(status_code=401, detail="Invalid Authentication.")
        return UserResponse(**user.__dict__)

    def get_user_by_id(self, user_id: UUID) -> UserResponse:
        """Fetch a user by id, or raise HTTPException(400) if not found."""
        user = self.__user_repo.get_user_by_id(user_id=user_id)

        if user:
            return UserResponse(**user.__dict__)
        raise HTTPException(status_code=400, detail="User is not available.")

    def get_user(self) -> UserResponse:
        """Fetch an arbitrary user record. Used by admin/debug flows."""
        user = self.__user_repo.get_user()

        if user:
            return UserResponse(**user.__dict__)
        raise HTTPException(status_code=400, detail="User not found.")
