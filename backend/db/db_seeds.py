from models.user import UserCreateRequest
from sqlalchemy.orm import Session
from utility.security.hash_helper import HashHelper


from logging import getLogger

logger = getLogger(__name__)

from typing import List


def get_users_seeds() -> List[UserCreateRequest]:
    users: List[UserCreateRequest] = []

    users.append(
        UserCreateRequest(
            first_name="Admin",
            last_name="Power",
            email="admin@playassist.com",
            password="password",
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
