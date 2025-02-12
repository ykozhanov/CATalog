from telebot import TeleBot    # type: ignore

from src.notification_service.telegram.settings import settings

bot = TeleBot(settings.bot_token)
