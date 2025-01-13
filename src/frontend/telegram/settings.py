import os

from dotenv import load_dotenv
load_dotenv()

from src.frontend.telegram.core.exceptions import ENVError
from src.frontend.telegram.core.exceptions.messages import MESSAGE_ENV_ERROR
from src.frontend.telegram.bot import bot


def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
        username=os.getenv("DB_USERNAME_FRONTEND_TELEGRAM"),
        password=os.getenv("DB_PASSWORD_FRONTEND_TELEGRAM"),
        host=host if host else os.getenv("DB_NAME_FRONTEND_TELEGRAM"),
        port=port if port else os.getenv("DB_HOST_FRONTEND_TELEGRAM"),
        dbname=os.getenv("DB_PORT_FRONTEND_TELEGRAM"),
    )


DEBUG=bool(os.getenv("DEBUG", "False"))

BOT_TOKEN=os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ENVError(f"{MESSAGE_ENV_ERROR}: не установлено значение 'BOT_TOKEN'")

BOT = bot

# AUTH_HEADER = "Authorization"

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")
