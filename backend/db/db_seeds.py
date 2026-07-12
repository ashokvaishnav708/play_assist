from models.user import UserCreateRequest
from sqlalchemy.orm import Session
from utility.security.hash_helper import HashHelper


from logging import getLogger

logger = getLogger(__name__)

from typing import List

from utility.utils import get_env_key

ADMIN_FIRST_NAME = get_env_key("ADMIN_FIRST_NAME", "Admin")
ADMIN_LAST_NAME = get_env_key("ADMIN_LAST_NAME", "Password")
ADMIN_EMAIL = get_env_key("ADMIN_EMAIL", "admin@playassist.com")
ADMIN_PASSWORD = get_env_key("ADMIN_PASSWORD", "password")


def get_users_seeds() -> List[UserCreateRequest]:
    users: List[UserCreateRequest] = []

    users.append(
        UserCreateRequest(
            first_name=ADMIN_FIRST_NAME,
            last_name=ADMIN_LAST_NAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            is_admin=True,
        )
    )

    return users


def execute_seeds(session: Session):
    from db.respository.user import UserRepository

    logger.info("Executing users seeds")
    # user seeds
    user_repo = UserRepository(session)
    users = get_users_seeds()
    for user in users:
        try:
            user.password = HashHelper.get_password_hash(user.password)
            user_repo.create_user(user)
        except Exception as e:
            logger.error(e)
    logger.info("Users seeds executed.")
