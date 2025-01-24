from telebot.types import Message

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.database.models import User
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.handlers.utils.messages import MESSAGES_COMMAND_LOGIN, MESSAGES_MAIN
from src.frontend.telegram.core.utils import SendMessage, crud
from src.frontend.telegram.bot.keyboards import KEYBOARD_YES_OR_NO
from src.frontend.telegram.bot.states import UsersStatesGroup
from . import COMMANDS


@BOT.message_handler(commands=[COMMANDS.start[0]])
def handle_command_start(message: Message) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    with MainDataContextmanager(message) as md:
        if md.user is None:
            user = crud.read(User, pk=msg_data.user_id)
            if user:
                md.user = user
                sm.send_message(text=MESSAGES_MAIN.message_start)
            else:
                sm.send_message(
                    text=MESSAGES_COMMAND_LOGIN.template_message_login(message.from_user.username),
                    inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
                    state=UsersStatesGroup.login,
                )
