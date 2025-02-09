from functools import wraps
from typing import Callable

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainMessages

def exc_handler_decorator(func: Callable[..., None]) -> Callable[..., None]:

    @wraps
    def wrapped(message: Message | CallbackQuery, *args, **kwargs) -> None:
        sm = SendMessage(message)
        main_m = MainMessages()
        try:
            return func(message, *args, **kwargs)
        except Exception as e:
            sm.send_message(main_m.t_got_exception(e), finish_state=True)

    return wrapped
