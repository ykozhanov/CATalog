import re

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.handlers.messages_helper import MESSAGES_MAIN, MESSAGES_COMMAND_LOGIN
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.keyboards import KEYBOARD_YES_OR_NO
from src.frontend.telegram.states import UsersStatesGroup
from src.frontend.telegram.api import UsersAPI, UserController
from src.frontend.telegram.core.exceptions import CreateUserError


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def login_user(message: Message | CallbackQuery) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    uc = UserController(telegram_user_id=msg_data.user_id)
    with MainDataContextmanager(message) as md:
        try:
            user_in_schema = UsersAPI().login_or_register(
                username=md.login.username,
                password=md.login.password,
                register_email=md.login.email,
            )
            uc.delete_user()
            user = uc.add_user(user_in_schema)
        except CreateUserError as e:
            sm.send_message(text=MESSAGES_COMMAND_LOGIN.template_message_got_exception(e), finish_state=True)
        else:
            md.user = user
            sm.send_message(
                text=MESSAGES_COMMAND_LOGIN.template_message_after_login(md.login.username),
                finish_state=True,
            )
            md.login = None


@BOT.message_handler(commands=["login"])
def handle_command_login(message: Message) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(
                text=MESSAGES_COMMAND_LOGIN.template_message_login(msg_data.username),
                inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
                state=UsersStatesGroup.login,
            )
        else:
            sm.send_message(text=MESSAGES_COMMAND_LOGIN.message_to_logout)


@BOT.callback_query_handler(state=UsersStatesGroup.login)
def handle_callback_login(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        text = MESSAGES_COMMAND_LOGIN.message_input_username
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.login.register = True
        text = MESSAGES_COMMAND_LOGIN.message_input_register_username
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
        return
    sm.send_message(text=text, state=UsersStatesGroup.waiting_username)


@BOT.message_handler(state=UsersStatesGroup.waiting_username)
def handle_state_waiting_username(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.login.username = message.text
        if md.login.register:
            text = MESSAGES_COMMAND_LOGIN.message_input_register_password
        else:
            text = MESSAGES_COMMAND_LOGIN.message_input_login_password
        sm.send_message(text=text, state=UsersStatesGroup.waiting_password)


@BOT.message_handler(state=UsersStatesGroup.waiting_password)
def handle_state_waiting_password(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.login.password = message.text
        register = md.login.register

    if register:
        sm.send_message(
            text=MESSAGES_COMMAND_LOGIN.message_input_register_password_repeat,
            state=UsersStatesGroup.waiting_password_repeat,
        )
    else:
        login_user(message)


@BOT.message_handler(state=UsersStatesGroup.waiting_password_repeat)
def handle_state_waiting_password_repeat(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        if md.login.password != message.text:
            sm.send_message(
                text=MESSAGES_COMMAND_LOGIN.message_input_invalid_register_password_repeat,
                state=UsersStatesGroup.waiting_password,
            )
        else:
            sm.send_message(
                text=MESSAGES_COMMAND_LOGIN.message_input_email,
                state=UsersStatesGroup.waiting_email,
            )


@BOT.message_handler(state=UsersStatesGroup.waiting_email)
def handle_state_waiting_email(message: Message) -> None:
    sm = SendMessage(message)
    email = message.text
    with MainDataContextmanager(message) as md:
        if is_valid_email(email):
            md.login.email = email
            if username := md.login.username:
                text = MESSAGES_COMMAND_LOGIN.template_message_check_register_md(
                        username=username,
                        email=md.login.email,
                    )
                sm.send_message(
                    text=text,
                    parse_mode="Markdown",
                    state=UsersStatesGroup.register_check_data,
                    inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
                )
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
        else:
            sm.send_message(text=MESSAGES_COMMAND_LOGIN.message_input_invalid_email)


@BOT.callback_query_handler(state=UsersStatesGroup.register_check_data)
def handle_callback_register_check_data(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        login_user(message)
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.login = None
            sm.send_message(
                text=MESSAGES_COMMAND_LOGIN.message_ask_register_again,
                state=UsersStatesGroup.ask_register_again,
                inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
            )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.callback_query_handler(state=UsersStatesGroup.ask_register_again)
def handle_callback_ask_register_again(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_COMMAND_LOGIN.message_input_register_username,
            state=UsersStatesGroup.waiting_username,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(text=MESSAGES_MAIN.message_to_login, finish_state=True)
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
