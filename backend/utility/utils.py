import os

from logging import getLogger

logger = getLogger(__name__)


def get_env_key(key: str, fallback_value: str | None = None) -> str | None:
    value = os.getenv(key)

    if not value:
        logger.error(
            f"Environment variable {key} not found, using fallback value {fallback_value}."
        )
        return fallback_value
    return value
