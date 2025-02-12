import os

from dotenv import load_dotenv
load_dotenv()

from src.backend.app import app
from src.backend.settings import BPS
from src.backend.core.exceptions import ENVError
from src.backend.core.exceptions.messages import MESSAGE_ENV_ERROR

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

for bp in BPS:
    app.register_blueprint(**bp)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))


JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
if not JWT_PUBLIC_KEY or not JWT_PRIVATE_KEY:
    raise ENVError(f"{MESSAGE_ENV_ERROR}: установите JWT_PRIVATE_KEY и JWT_PUBLIC_KEY")

JWT_ALGORITHM = "RS256"

AUTH_HEADER = "Authorization"

REDIS_HOSTNAME_CACHE_B = os.getenv("REDIS_HOSTNAME_CACHE_B")
REDIS_PORT_CACHE_B = os.getenv("REDIS_PORT_CACHE_B")
REDIS_DB_CACHE_B = os.getenv("REDIS_DB_CACHE_B")
REDIS_PASSWORD_CACHE_B = os.getenv("REDIS_PASSWORD_CACHE_B")

def redis_cache_url() -> str:
    if not REDIS_HOSTNAME_CACHE_B or not REDIS_PORT_CACHE_B or not REDIS_DB_CACHE_B:
        raise ENVError(f"{MESSAGE_ENV_ERROR}: установите REDIS_HOSTNAME_CACHE_B, REDIS_PORT_CACHE_B и REDIS_PASSWORD_CACHE_B")
    if REDIS_PASSWORD_CACHE_B is not None:
        return f"redis://:{REDIS_PASSWORD_CACHE_B}@{REDIS_HOSTNAME_CACHE_B}:{REDIS_PORT_CACHE_B}/{REDIS_DB_CACHE_B}"
    return f"redis://{REDIS_HOSTNAME_CACHE_B}:{REDIS_PORT_CACHE_B}/{REDIS_DB_CACHE_B}"
