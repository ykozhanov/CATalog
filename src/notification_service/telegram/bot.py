from telebot import TeleBot    # type: ignore

from src.notification_service.telegram.settings import Settings

bot = TeleBot(Settings.bot_token)
