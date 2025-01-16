from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.handlers.messages_helper import MESSAGES_COMMAND_LOGOUT, MESSAGES_MAIN
from src.frontend.telegram.keyboards import KEYBOARD_YES_OR_NO
from src.frontend.telegram.states import UsersStatesGroup
from src.frontend.telegram.api import UserController
from . import COMMANDS


@BOT.message_handler(commands=[COMMANDS.logout[0]])
def handle_command_logout(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(text=MESSAGES_COMMAND_LOGOUT.message_to_login, finish_state=True)
            return
    sm.send_message(
        text=MESSAGES_COMMAND_LOGOUT.message_ask_logout,
        inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        state=UsersStatesGroup.ask_logout,
    )


@BOT.message_handler(commands=[COMMANDS.logout[0]])
def handle_ask_logout(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.user = None
        UserController(telegram_user_id=msg_data.user_id).delete_user()
        sm.send_message(text=MESSAGES_COMMAND_LOGOUT.message_callback_yes, finish_state=True)
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(text=MESSAGES_COMMAND_LOGOUT.message_callback_no, finish_state=True)
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
