import re

from telebot.types import Message, CallbackQuery

from src.db_lib.base.exceptions.base_exceptions import NotFoundInDBError
from src.frontend.telegram.api.users.users_api import UsersAPI
from src.frontend.telegram.api.users.users_controller import UserController
from src.frontend.telegram.handlers.utils import MainDataContextmanager
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.broker_kafka import UserSubject

from .messages import LoginCommandTemplates

templates = LoginCommandTemplates()


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


def login_user(message: Message | CallbackQuery) -> None:
    sm = SendMessage(message)
    msg_data = sm.get_message_data()
    uc = UserController(telegram_user_id=msg_data.user_id)
    u_api = UsersAPI()
    with MainDataContextmanager(message) as md:
        user_in_schema = u_api.login_or_register(
            username=md.login.username,
            password=md.login.password,
            register_email=md.login.email,
        )
        try:
            uc.delete_user()
        except NotFoundInDBError:
            pass
        user = uc.add_user(user_in_schema)
        md.user = user
        UserSubject(
            user_id=msg_data.user_id,
            chat_id=msg_data.chat_id,
            refresh_token=user.refresh_jtw_token,
        ).create_user()
        sm.send_message(
            text=templates.after_login(md.login.username),
            finish_state=True,
        )
        md.login = None
