from telebot import custom_filters

import frontend.telegram_bot.handlers  # noqa: F401

from .bot import telegram_bot

if __name__ == "__main__":
    telegram_bot.add_custom_filter(custom_filters.StateFilter(telegram_bot))
    telegram_bot.polling(none_stop=True)
