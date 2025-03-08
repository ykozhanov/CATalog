import bcrypt


class HashPWMixin:

    @staticmethod
    def _hashpw(password: str) -> bytes:
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    @staticmethod
    def _check_hashpw(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
