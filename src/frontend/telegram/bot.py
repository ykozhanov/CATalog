from telebot import TeleBot    # type: ignore

from .settings import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)
