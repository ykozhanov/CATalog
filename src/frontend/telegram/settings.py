import os

from dotenv import load_dotenv
load_dotenv()

from .core.exceptions import ENVError

DEBUG=bool(os.getenv("DEBUG", "False"))

BOT_TOKEN=os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ENVError("Установите значение BOT_TOKEN")
