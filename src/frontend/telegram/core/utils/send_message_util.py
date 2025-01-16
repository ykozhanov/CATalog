from dataclasses import dataclass

from telebot.states import State
from telebot.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from telegram_bot_pagination import InlineKeyboardPaginator

from src.frontend.telegram.core.exceptions import CreateMessageError
from src.frontend.telegram.core.exceptions.messages import MESSAGE_CREATE_MESSAGE_ERROR
from src.frontend.telegram.settings import BOT


# from typing import Literal
# KeyboardType = Literal["inline", "reply", "paginator"]
# KEYBOARD_INLINE: KeyboardType = "inline"
# KEYBOARD_REPLY: KeyboardType = "reply"
# KEYBOARD_PAGINATOR: KeyboardType = "paginator"


@dataclass
class MessageData:
    user_id: int
    chat_id: int
    message_id: int
    username: str


class GetMessageData:

    def __init__(self, message: Message | CallbackQuery):
        self._message = message

    def get_message_data(self) -> MessageData:
        if isinstance(self._message, Message):
            return MessageData(
                user_id=self._message.from_user.id,
                chat_id=self._message.chat.id,
                message_id=self._message.message_id,
                username=self._message.from_user.username,
            )
        return MessageData(
            user_id=self._message.from_user.id,
            chat_id=self._message.message.chat.id,
            message_id=self._message.message.message_id,
            username=self._message.from_user.username,
        )


class SendMessage(GetMessageData):

    def __init__(
            self,
            message: Message | CallbackQuery,
    ):
        super().__init__(message=message)
        self.msg_data = self.get_message_data()

    @staticmethod
    def _get_reply_keyboard(reply_keyboard_data: list[str]) -> ReplyKeyboardMarkup:
        if reply_keyboard_data is None:
            raise CreateMessageError(f"{MESSAGE_CREATE_MESSAGE_ERROR}: не передан аргумент 'reply_keyboard_data'")
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for text in reply_keyboard_data:
            keyboard.add(KeyboardButton(text))
        return keyboard

    @staticmethod
    def _get_inline_keyboard(inline_keyboard_data: list[tuple[str, str]] | InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        if inline_keyboard_data is None:
            raise CreateMessageError(f"{MESSAGE_CREATE_MESSAGE_ERROR}: не передан аргумент 'inline_keyboard_data'")
        if isinstance(inline_keyboard_data, InlineKeyboardMarkup):
            return inline_keyboard_data
        keyboard = InlineKeyboardMarkup()
        for text, callback_data in inline_keyboard_data:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))
        return keyboard

    def _get_reply_markup(
            self,
            reply_keyboard: list[str] | None,
            inline_keyboard: list[tuple[str, str]] | InlineKeyboardMarkup | None,
            delete_reply_keyboard: bool | None,
    ) -> ReplyKeyboardMarkup | InlineKeyboardMarkup | InlineKeyboardPaginator | ReplyKeyboardRemove | None:
        if reply_keyboard:
            return self._get_reply_keyboard(reply_keyboard)
        if inline_keyboard:
            return self._get_inline_keyboard(inline_keyboard)
        if delete_reply_keyboard:
            return ReplyKeyboardRemove()
        return None

    def set_state(self, state: State | None) -> None:
        BOT.set_state(
            user_id=self.msg_data.user_id,
            state=state,
            chat_id=self.msg_data.chat_id,
        )

    def delete_message(self) -> None:
        BOT.delete_message(chat_id=self.msg_data.chat_id, message_id=self.msg_data.message_id)

    def delete_reply_keyboard(self) -> None:
        BOT.edit_message_reply_markup(
            chat_id=self.msg_data.chat_id,
            message_id=self.msg_data.message_id,
            reply_markup=None,
        )

    def send_message(
            self,
            text: str,
            parse_mode: str | None = None,
            state: State | None = None,
            finish_state: bool = False,
            inline_keyboard: list[tuple[str, str]] | InlineKeyboardMarkup = None,
            reply_keyboard: list[str] | None = None,
            delete_reply_keyboard: bool = False,
    ) -> None:
        reply_markup = self._get_reply_markup(
            inline_keyboard=inline_keyboard,
            reply_keyboard=reply_keyboard,
            delete_reply_keyboard=delete_reply_keyboard,
        )
        if state or finish_state:
            self.set_state(state)
        BOT.send_message(
            chat_id=self.msg_data.chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
