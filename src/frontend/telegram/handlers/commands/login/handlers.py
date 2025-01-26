from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.handlers.utils import MainDataContextmanager, MainMessages
from src.frontend.telegram.handlers.utils.md_dataclasses import LoginDataclass
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import UsersStatesGroup
from .utils import is_valid_email, login_user
from .messages import LoginCommandMessages, LoginCommandTemplates

main_m = MainMessages()
messages = LoginCommandMessages()
templates = LoginCommandTemplates()
y_or_n = KeyboardYesOrNo()


@BOT.message_handler(commands=["login"])
def handle_command_login(message: Message) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    with MainDataContextmanager(message) as md:
        if md.user is None:
            sm.send_message(
                templates.login_or_register(msg_data.username),
                inline_keyboard=y_or_n.get_inline_keyboard(),
                state=UsersStatesGroup.login,
            )
        else:
            sm.send_message(messages.to_logout)


@BOT.callback_query_handler(state=UsersStatesGroup.login)
def handle_callback_login(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == y_or_n.callback_answer_yes:
        text = messages.input_username
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.login = LoginDataclass()
            md.login.register = True
        text = messages.input_register_username
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
        return
    sm.send_message(text=text, state=UsersStatesGroup.waiting_username)


@BOT.message_handler(state=UsersStatesGroup.waiting_username)
def handle_state_waiting_username(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.login.username = message.text
        if md.login.register:
            text = messages.input_register_password
        else:
            text = messages.input_login_password
        sm.send_message(text, state=UsersStatesGroup.waiting_password)


@BOT.message_handler(state=UsersStatesGroup.waiting_password)
def handle_state_waiting_password(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.login.password = message.text
        register = md.login.register

    if register:
        sm.send_message(
            text=messages.input_register_password_repeat,
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
                text=messages.input_register_password_repeat,
                state=UsersStatesGroup.waiting_password,
            )
        else:
            sm.send_message(
                text=messages.input_email,
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
                sm.send_message(
                    text=templates.check_md(username=username, email=md.login.email),
                    parse_mode="Markdown",
                    state=UsersStatesGroup.register_check_data,
                    inline_keyboard=y_or_n.get_inline_keyboard(),
                )
            else:
                sm.send_message(main_m.something_went_wrong, finish_state=True)
                return
        else:
            sm.send_message(messages.invalid_email)


@BOT.callback_query_handler(state=UsersStatesGroup.register_check_data)
def handle_callback_register_check_data(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == y_or_n.callback_answer_yes:
        login_user(message)
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.login = None
            sm.send_message(
                messages.ask_register_again,
                state=UsersStatesGroup.ask_register_again,
                inline_keyboard=y_or_n.get_inline_keyboard(),
            )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)


@BOT.callback_query_handler(state=UsersStatesGroup.ask_register_again)
def handle_callback_ask_register_again(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_register_username, state=UsersStatesGroup.waiting_username)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(main_m.to_login, finish_state=True)
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
