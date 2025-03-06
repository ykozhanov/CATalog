from telebot.types import Message

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainDataContextmanager, MainMessages
from src.frontend.telegram.bot.keyboards import KeyboardListActions
from src.frontend.telegram.bot.states import ActionsStatesGroup
from src.frontend.telegram.handlers.commands import COMMANDS
from .messages import HelpCommandMessages

__all__ = ["handle_command_help"]

main_m = MainMessages()
messages = HelpCommandMessages()


@telegram_bot.message_handler(commands=[COMMANDS.help[0]])
def handle_command_help(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(main_m.to_login, finish_state=True)
            return
    sm.send_message(
        messages.list_actions,
        reply_keyboard=KeyboardListActions.get_reply_keyboard(),
        finish_state=ActionsStatesGroup.choosing_action,
    )
