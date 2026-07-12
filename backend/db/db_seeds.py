from models.user import UserCreateRequest
from sqlalchemy.orm import Session


from logging import getLogger

logger = getLogger(__name__)

from typing import List


def get_users_seeds() -> List[UserCreateRequest]:
    users: List[UserCreateRequest] = []

    users.append(
        UserCreateRequest(
            first_name="Admin",
            last_name="Power",
            email="admin@play_assist.com",
            password="password",
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
            user_repo.create_user(user)
        except Exception as e:
            logger.error(e)
    logger.info("Users seeds executed.")
