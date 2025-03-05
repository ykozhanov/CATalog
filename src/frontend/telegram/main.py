from telebot.custom_filters import StateFilter

from .bot import telegram_bot
from .handlers.commands.start.handlers import handle_command_start

if __name__ == "__main__":
    telegram_bot.add_custom_filter(StateFilter(telegram_bot))
    telegram_bot.polling(none_stop=True)