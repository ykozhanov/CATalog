import bcrypt


def hashpw(password: str) -> bytes:
    return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())


def check_hashpw(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

hpwd = hashpw("test")

print(check_hashpw("test", hpwd))
