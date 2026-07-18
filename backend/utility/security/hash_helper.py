"""Password hashing/verification via bcrypt."""

from bcrypt import checkpw, hashpw, gensalt

class HashHelper(object):
    """Static helpers for hashing and verifying user passwords."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Check a plaintext password against a bcrypt hash."""
        return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def get_password_hash(plain_password: str) -> str:
        """Hash a plaintext password with a fresh bcrypt salt."""
        return hashpw(
            plain_password.encode('utf-8'),
            gensalt()
        ).decode('utf-8')