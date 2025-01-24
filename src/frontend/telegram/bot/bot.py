from telebot import TeleBot    # type: ignore

from src.frontend.telegram.settings import BOT_TOKEN

telegram_bot = TeleBot(BOT_TOKEN)
