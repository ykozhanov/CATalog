from telebot.custom_filters import StateFilter

from .bot import telegram_bot

from .settings import DEBUG
if DEBUG:
    import logging

    logging.basicConfig(
        level=logging.DEBUG,  # Уровень логирования
        format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщения
        handlers=[
            logging.StreamHandler(),  # Вывод в консоль
        ]
    )

from .handlers import *


if __name__ == "__main__":
    telegram_bot.add_custom_filter(StateFilter(telegram_bot))
    telegram_bot.polling(none_stop=True)
