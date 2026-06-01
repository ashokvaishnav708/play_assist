from utility.utils import get_env_key
import time
import jwt
from logging import getLogger

logger = getLogger(__name__)

JWT_SECRET = get_env_key("JWT_SECRET")
JWT_ALGORITHM = get_env_key("JWT_ALGORITHM")

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 900
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    

    @staticmethod
    def deode_jwt(token: str) -> dict | None:
        try:
            decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            expire_time = decode_token["expires"]

            if expire_time >= time.time():
                return expire_time
            else: 
                return None
        except:
            logger.error("Unable to decode token.")
            return None