import logging
from telebot.types import Message

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import UsersStatesGroup
from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.handlers.commands.login.messages import LoginCommandTemplates
from src.frontend.telegram.api import UserController
from .messages import StartCommandMessages

__all__ = ["handle_command_start"]

messages = StartCommandMessages()
templates_login = LoginCommandTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.message_handler(commands=[COMMANDS.start[0]])
def handle_command_start(message: Message) -> None:
    logging.info("Старт 'handle_command_start'")
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    with MainDataContextmanager(message) as md:
        if md.user is None:
            user = UserController(telegram_user_id=msg_data.user_id).get_user()
            logging.debug(f"user: {user}")
            if user:
                md.user = user
                logging.debug(f"md.user: {user}")
                sm.send_message(messages.start)
                logging.debug(f"chat_id: {msg_data.chat_id} | user_id: {msg_data.user_id}")
                logging.info("Конец 'handle_command_start'")
            else:
                sm.send_message(
                    templates_login.login_or_register(msg_data.username),
                    inline_keyboard=y_or_n.get_inline_keyboard(),
                    state=UsersStatesGroup.login,
                )
                logging.info("Конец 'handle_command_start'")
        else:
            sm.send_message(messages.start)
            logging.info("Конец 'handle_command_start'")
