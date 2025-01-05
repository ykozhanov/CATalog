import bcrypt


class HashPWMixin:

    @staticmethod
    def _hashpw(password: str) -> bytes:
        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())

    @staticmethod
    def _check_hashpw(hashed_password: bytes, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password)
