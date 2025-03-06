import time

from telebot.custom_filters import StateFilter

from .bot import telegram_bot
from .handlers import *

if __name__ == "__main__":
    telegram_bot.add_custom_filter(StateFilter(telegram_bot))
    telegram_bot.polling(none_stop=True)
