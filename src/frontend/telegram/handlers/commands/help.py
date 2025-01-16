from telebot.types import Message

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.handlers.messages_helper import MESSAGES_COMMAND_HELP
from src.frontend.telegram.keyboards import KEYBOARD_LIST_ACTIONS
from src.frontend.telegram.states import ActionsStatesGroup
from . import COMMANDS


@BOT.message_handler(commands=[COMMANDS.help[0]])
def handle_command_help(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(text=MESSAGES_COMMAND_HELP.message_to_login, finish_state=True)
            return
    sm.send_message(
        text=MESSAGES_COMMAND_HELP.message_list_actions,
        reply_keyboard=KEYBOARD_LIST_ACTIONS.get_reply_keyboard(),
        finish_state=ActionsStatesGroup.choosing_action,
    )
