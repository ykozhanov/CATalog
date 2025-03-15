from typing import Callable
from functools import wraps

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.api import UserController
from src.frontend.telegram.core.utils import SendMessage
from .messages import MainMessages
from .main_data_contextmanager import MainDataContextmanager

main_m = MainMessages()


def get_message(args: tuple) -> CallbackQuery | Message | None:
    for a in args:
        if isinstance(a, CallbackQuery) or isinstance(a, Message):
            return a
    return None


def login_func(message: CallbackQuery | Message) -> None:
    msg_data = SendMessage(message).msg_data
    with MainDataContextmanager(message) as md:
        md_user = md.user
    if md_user is None:
        user = UserController(telegram_user_id=msg_data.user_id).get_user()
        if user:
            with MainDataContextmanager(message) as md:
                md.user = user


def check_login_decorator(func: Callable[..., None]) -> Callable[..., None]:

    @wraps(func)
    def wrapped(*args, **kwargs):
        message = get_message(args)
        if message is None:
            return func(*args, **kwargs)
        login_func(message)
        return func(*args, **kwargs)

    return wrapped
