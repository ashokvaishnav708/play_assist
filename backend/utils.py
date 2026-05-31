import os

from logging import getLogger
logger = getLogger(__name__)


def get_env_key(key: str) -> str | None:
    value = os.getenv(key)

    if not value:
        logger.error(f"Environment variable {key} not found.")
        return None
    return value