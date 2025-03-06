from telebot.types import Message, CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainDataContextmanager, MainMessages
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import UsersStatesGroup
from src.frontend.telegram.api import UserController
from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.broker_kafka import UserSubject

from .messages import LogoutCommandMessages

__all__ = ["handle_command_logout"]

main_m = MainMessages()
messages = LogoutCommandMessages()
y_or_n = KeyboardYesOrNo()


@telegram_bot.message_handler(commands=[COMMANDS.logout[0]])
def handle_command_logout(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(main_m.to_login, finish_state=True)
            return
    sm.send_message(
        messages.ask_logout,
        inline_keyboard=y_or_n.get_inline_keyboard(),
        state=UsersStatesGroup.ask_logout,
    )


@telegram_bot.message_handler(commands=[COMMANDS.logout[0]])
def handle_ask_logout(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.user = None
        UserController(telegram_user_id=msg_data.user_id).delete_user()
        UserSubject(user_id=msg_data.user_id, chat_id=msg_data.chat_id).delete_user()
        sm.send_message(messages.callback_yes, finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(messages.callback_no, finish_state=True)
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)
