import os

from dotenv import load_dotenv
load_dotenv()

from src.frontend.telegram.core.exceptions import ENVError
from src.frontend.telegram.core.exceptions.messages import MESSAGE_ENV_ERROR
from src.frontend.telegram.bot import telegram_bot


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

BOT = telegram_bot

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")

APP_NAME = os.getenv("APP_NAME", "CATalog")

DISPLAY_DATE_FORMATE = "%Y.%m.%d"

EXP_DAYS = int(os.getenv("EXP_DAYS", "3"))

ITEMS_PER_PAGE = 5

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC_ADD_NEW_USER = "new_telegram_user"
KAFKA_TOPIC_DELETE_USER = "delete_telegram_user"

KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")

TOKEN_CRYPT_KEY=os.getenv("TOKEN_CRYPT_KEY", "mUkruC7uY382ZKIgYZZC6NAwyhDzgTDblnyIrrP6rrQ").encode("utf-8")
