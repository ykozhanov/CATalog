from telebot.types import Message, CallbackQuery

from src.frontend.telegram.core.utils import GetMessageData
from src.frontend.telegram.settings import BOT
from src.frontend.telegram.handlers.utils.md_dataclasses import MainDataclass

KEY_MAIN_DATA_IN_RETRIEVE_DATA = "main_data"


class MainDataContextmanager:

    def __init__(self, message: Message | CallbackQuery):
        self._message = message
        self._msg_data = GetMessageData(message=message).get_message_data()

    def __enter__(self):
        with BOT.retrieve_data(user_id=self._msg_data.user_id, chat_id=self._msg_data.chat_id) as self._data:
            self._main_data: MainDataclass = self._data.get(KEY_MAIN_DATA_IN_RETRIEVE_DATA, MainDataclass())
            return self._main_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._data[KEY_MAIN_DATA_IN_RETRIEVE_DATA] = self._main_data
