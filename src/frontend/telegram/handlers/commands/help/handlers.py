import logging

from telebot.types import Message

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainDataContextmanager, MainMessages
from src.frontend.telegram.bot.keyboards import k_list_actions
from src.frontend.telegram.bot.states import ActionsStatesGroup
from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.handlers.commands.login.utils import login_user
from .messages import HelpCommandMessages

__all__ = ["handle_command_help"]

main_m = MainMessages()
messages = HelpCommandMessages()


@telegram_bot.message_handler(commands=[COMMANDS.help[0]])
def handle_command_help(message: Message) -> None:
    logging.info("Старт 'handle_command_help'")
    sm = SendMessage(message)
    logging.debug(f"chat_id: {sm.msg_data.chat_id} | user_id: {sm.msg_data.user_id}")
    with MainDataContextmanager(message) as md:
        logging.debug(f"md.user: {md.user}")
        if md.user is None:
            sm.send_message(main_m.to_login, finish_state=True)
            logging.debug(f"Установлено состояние: {telegram_bot.get_state(sm.get_message_data().user_id)}")
            logging.info("Конец 'handle_command_help'")
            return
    sm.send_message(
        messages.list_actions,
        reply_keyboard=k_list_actions.get_reply_keyboard(),
        state=ActionsStatesGroup.choosing_action,
    )
    logging.debug(f"Установлено состояние: {telegram_bot.get_state(sm.msg_data.user_id)}")
    logging.info("Конец 'handle_command_help'")
