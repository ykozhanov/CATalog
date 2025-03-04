from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import telegram_bot
from src.frontend.telegram.core.utils import SendMessage, PaginatorListHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import CategoryDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import CategoriesStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.api.categories.schemas import CategoryOutSchema
from .messages import CategoryCreateActionTemplates, CategoryCreateActionMessages, MAX_LEN_NAME
from .states import CategoryCreateStatesGroup

main_m = MainMessages()
messages = CategoryCreateActionMessages()
templates = CategoryCreateActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.callback_query_handler(
    func=lambda m: m.data == PaginatorListHelper.CALLBACK_CREATE,
    state=CategoriesStatesGroup.categories,
)
def handle_paginator_category_create_new_category(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        md.category = CategoryDataclass()
    sm = SendMessage(message)
    sm.delete_message()
    sm.send_message(
        text=messages.input_name,
        state=CategoryCreateStatesGroup.waiting_input_name,
    )


@telegram_bot.callback_query_handler(state=CategoryCreateStatesGroup.ask_add_new)
def handle_category_create_ask_add_new(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.product = CategoryDataclass()
        sm.send_message(
            text=messages.input_name,
            state=CategoryCreateStatesGroup.waiting_input_name,
        )
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(text=main_m.to_help, finish_state=True)
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=CategoryCreateStatesGroup.waiting_input_name)
def handle_category_create_waiting_input_name(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NAME:
        return sm.send_message(templates.error_max_len(MAX_LEN_NAME))
    with MainDataContextmanager(message) as md:
        md.category.name = name = message.text
    sm.send_message(
        text=templates.check_md(name),
        state=CategoryCreateStatesGroup.check_new,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@exc_handler_decorator
@check_authentication_decorator
@telegram_bot.callback_query_handler(state=CategoryCreateStatesGroup.check_new)
def handle_product_category_check_new_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            category_data = md.category
            if a_token := md.user.access_jtw_token is None:
                return sm.send_message(main_m.something_went_wrong, finish_state=True)
        c_api = CategoriesAPI(a_token)
        category = CategoryOutSchema(**category_data.dict())
        c_api.post(category)
        with MainDataContextmanager(message) as md:
            md.category = None
        sm.send_message(messages.success, finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product = None
        sm.send_message(
            messages.try_again,
            state=CategoryCreateStatesGroup.ask_add_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
