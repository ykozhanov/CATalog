from functools import wraps
from typing import Callable

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import MainMessages
from src.frontend.telegram.core.exceptions import CreateMessageError
from src.frontend.telegram.api.products.exceptions import ProductError
from src.frontend.telegram.api.categories.exceptions import CategoryError
from src.frontend.telegram.api.users.exceptions import CreateUserError


def exc_handler_decorator(func: Callable[..., None]) -> Callable[..., None]:

    @wraps
    def wrapped(message: Message | CallbackQuery, *args, **kwargs) -> None:
        sm = SendMessage(message)
        main_m = MainMessages()
        try:
            return func(message, *args, **kwargs)
        except (CreateMessageError, CreateUserError, CategoryError, ProductError) as e:
            sm.send_message(main_m.t_got_exception(e), finish_state=True)
        except Exception as e:
            raise e

    return wrapped
