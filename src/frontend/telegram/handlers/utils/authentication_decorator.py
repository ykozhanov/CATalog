from typing import Callable
from functools import wraps

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.core.exceptions import AuthenticationError
from src.frontend.telegram.api import UsersAPI, UserController
from src.frontend.telegram.core.utils import SendMessage
from .messages import MainMessages
from .main_data_contextmanager import MainDataContextmanager


def get_message(args: tuple) -> CallbackQuery | Message | None:
    for a in args:
        if isinstance(a, CallbackQuery) or isinstance(a, Message):
            return a
    return None


def check_authentication_decorator(func: Callable[..., None]) -> Callable[..., None]:

    @wraps
    def wrapped(*args, **kwargs):
        if message := get_message(args) is None:
            return func(*args, **kwargs)
        sm = SendMessage(message)
        msg_data = sm.get_message_data()
        main_m = MainMessages()
        try:
            result = func(*args, **kwargs)
        except AuthenticationError:
            try:
                with MainDataContextmanager(message) as md:
                    if md.user is None:
                        sm.send_message(text=main_m.to_login, finish_state=True)
                        return
                user_in_schema = UsersAPI.token(refresh_jwt_token=md.user.refresh_jtw_token)
                uc = UserController(telegram_user_id=msg_data.user_id)
                uc.delete_user()
                user = uc.add_user(user_in_schema=user_in_schema)
                with MainDataContextmanager(message) as md:
                    md.user = user
            except AuthenticationError:
                sm.send_message(text=main_m.to_login, finish_state=True)
            else:
                return func(*args, **kwargs)
        else:
            return result

    return wrapped
