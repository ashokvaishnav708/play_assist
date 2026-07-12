from utility.utils import get_env_key
from uuid import UUID
import time
import jwt
from logging import getLogger

logger = getLogger(__name__)

JWT_SECRET = get_env_key("JWT_SECRET")
JWT_ALGORITHM = get_env_key("JWT_ALGORITHM")

DEFAULT_EXPIRY_SECONDS = 900 # 15 minutes

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id: UUID, expiry: float | None = None, refresh: bool = False) -> str:
        payload = {
            # UUID is not JSON-serializable, so PyJWT needs it as a string
            "user_id": str(user_id),
            "expires": time.time() + (expiry if expiry is not None else DEFAULT_EXPIRY_SECONDS)
        }

        payload["refresh"] = refresh

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    

    @staticmethod
    def deode_jwt(token: str) -> dict | None:
        try:
            decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            expire_time = decode_token["expires"]

            if expire_time >= time.time():
                return decode_token
            else: 
                return None
        except:
            logger.error("Unable to decode token.")
            return None