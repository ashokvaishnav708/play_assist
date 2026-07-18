"""JWT issuing/decoding for access and refresh tokens."""

from utility.utils import get_env_key
from uuid import UUID
import time
import jwt
from logging import getLogger

logger = getLogger(__name__)

JWT_SECRET = get_env_key("JWT_SECRET")
JWT_ALGORITHM = get_env_key("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRY_SECONDS = 900               # 15 minutes
REFRESH_TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 7  # 7 days


class TokenExpiredError(Exception):
    """Raised when a JWT's exp claim has passed."""

    pass


class TokenInvalidError(Exception):
    """Raised when a JWT fails signature/format validation."""

    pass


class AuthHandler(object):
    """Static helpers for signing and decoding access/refresh JWTs."""

    @staticmethod
    def sign_jwt(user_id: UUID, token_version: int, expiry: float | None = None, refresh: bool = False) -> str:
        """Create a signed JWT for the given user.

        Defaults expiry based on whether this is an access or refresh token,
        and stamps the user's current token_version so it can be invalidated
        wholesale on logout.
        """
        if expiry is None:
            expiry = REFRESH_TOKEN_EXPIRY_SECONDS if refresh else ACCESS_TOKEN_EXPIRY_SECONDS

        payload = {
            # UUID is not JSON-serializable, so PyJWT needs it as a string
            "user_id": str(user_id),
            "token_version": token_version,
            "refresh": refresh,
            "exp": int(time.time() + expiry),
        }

        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_jwt(token: str) -> dict:
        """Decode and verify a JWT, raising TokenExpiredError/TokenInvalidError on failure."""
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            logger.error("Unable to decode token.")
            raise TokenInvalidError()
