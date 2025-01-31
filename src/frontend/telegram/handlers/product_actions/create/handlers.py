from datetime import datetime

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage, PaginatorListHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import ProductDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import ProductsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.api.products.schemas import ProductOutSchema
from src.frontend.telegram.handlers.actions.get_all_categories.utils import PREFIX_CATEGORY_ELEMENT_PAGINATOR
from .messages import (
    ProductCreateActionMessages,
    ProductCreateActionTemplates,
    MAX_LEN_NOTE,
    MAX_LEN_UNIT,
    MAX_LEN_NAME,
)
from .utils import get_inline_categories
from .states import ProductCreateStatesGroup

main_m = MainMessages()
messages = ProductCreateActionMessages()
templates = ProductCreateActionTemplates()
y_or_n = KeyboardYesOrNo()


@BOT.callback_query_handler(
    func=lambda m: m.data == PaginatorListHelper.CALLBACK_CREATE,
    state=ProductsStatesGroup.products,
)
def handle_paginator_create_new_product(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        md.product = ProductDataclass()
    sm = SendMessage(message)
    sm.delete_message()
    sm.send_message(
        text=messages.input_name,
        state=ProductCreateStatesGroup.waiting_input_name,
    )


@BOT.callback_query_handler(state=ProductCreateStatesGroup.ask_add_new)
def handle_ask_add_new_product(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.product = ProductDataclass()
        sm.send_message(
            text=messages.input_name,
            state=ProductCreateStatesGroup.waiting_input_name,
        )
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(text=main_m.to_help, finish_state=True)
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_name)
def handle_product_create_waiting_input_name(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NAME:
        return sm.send_message(templates.error_max_len(MAX_LEN_NAME))
    with MainDataContextmanager(message) as md:
        md.product.name = message.text
    sm.send_message(
        text=messages.input_unit,
        state=ProductCreateStatesGroup.waiting_input_unit,
    )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_unit)
def handle_product_create_waiting_input_unit(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_UNIT:
        return sm.send_message(templates.error_max_len(MAX_LEN_UNIT))
    with MainDataContextmanager(message) as md:
        md.product.unit = message.text
    sm.send_message(
        text=messages.input_quantity,
        state=ProductCreateStatesGroup.waiting_input_quantity,
    )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_quantity)
def handle_product_create_waiting_input_quantity(message: Message):
    sm = SendMessage(message)
    try:
        if quantity := float(message.text.replace(",", ".")) < 0:
            raise ValueError()
    except ValueError:
        return sm.send_message(messages.error_quantity)
    else:
        with MainDataContextmanager(message) as md:
            md.product.quantity = quantity
        sm.send_message(
            text=messages.ask_input_exp_date,
            state=ProductCreateStatesGroup.ask_input_exp_date,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )


@BOT.callback_query_handler(state=ProductCreateStatesGroup.ask_input_exp_date)
def handle_product_create_ask_input_exp_date(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_day, state=ProductCreateStatesGroup.waiting_input_day)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(
            text=messages.ask_input_note,
            state=ProductCreateStatesGroup.ask_input_note,
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_day)
def handle_product_create_waiting_input_day(message: Message):
    sm = SendMessage(message)
    try:
        day = int(message.text)
        if 31 < day < 1:
            raise ValueError
    except ValueError:
        sm.send_message(messages.error_day)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_day = day
        sm.send_message(
            text=messages.input_month,
            state=ProductCreateStatesGroup.waiting_input_month,
        )

@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_month)
def handle_product_create_waiting_input_month(message: Message):
    sm = SendMessage(message)
    try:
        month = int(message.text)
        if 12 < month < 1:
            raise ValueError
    except ValueError:
        sm.send_message(messages.error_month)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_month = month
        sm.send_message(
            text=messages.input_year,
            state=ProductCreateStatesGroup.waiting_input_year,
        )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_year)
def handle_product_create_waiting_input_year(message: Message):
    sm = SendMessage(message)
    try:
        year = datetime.strptime(message.text, "%y").year
    except ValueError:
        sm.send_message(messages.error_year)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_year = year
            exp_date = datetime(year, month=md.product.exp_date_month, day=md.product.exp_date_day).date()
            md.product.exp_date = exp_date
        sm.send_message(
            text=messages.ask_input_note,
            state=ProductCreateStatesGroup.ask_input_note,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )


@exc_handler_decorator
@check_authentication_decorator
@BOT.callback_query_handler(state=ProductCreateStatesGroup.ask_input_note)
def handle_product_create_ask_input_note(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_note, state=ProductCreateStatesGroup.waiting_input_note)
    elif message.data == y_or_n.callback_answer_no:
        inline_keyboard = get_inline_categories(message)
        sm.send_message(
            text=messages.choice_category,
            state=ProductCreateStatesGroup.waiting_choice_category,
            inline_keyboard=inline_keyboard,
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@exc_handler_decorator
@check_authentication_decorator
@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_note)
def handle_product_create_waiting_input_note(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NOTE:
        return sm.send_message(templates.error_max_len(MAX_LEN_NOTE))
    with MainDataContextmanager(message) as md:
        md.product.note = message.text
        category_id = md.product.category_id
        category_name = md.product.category_name
    inline_keyboard = get_inline_categories(message)
    if category_id is None or category_name is None:
        sm.send_message(
            messages.choice_category,
            state=ProductCreateStatesGroup.waiting_choice_category,
            inline_keyboard=inline_keyboard,
        )
    else:
        with MainDataContextmanager(message) as md:
            name = md.product.name
            unit = md.product.unit
            quantity = md.product.quantity
            exp_date = md.product.exp_date
            note = md.product.note
            category = md.product.category_name
        sm.send_message(
            templates.check_md(name, unit, quantity, exp_date, note, category),
            state=ProductCreateStatesGroup.check_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )


@BOT.callback_query_handler(state=ProductCreateStatesGroup.waiting_choice_category)
def handle_product_create_waiting_category(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data.split("#")[0] == PREFIX_CATEGORY_ELEMENT_PAGINATOR:
        category_id, category_name = message.data.split("#")[1:]
        with MainDataContextmanager(message) as md:
            md.product.category_id = category_id
            md.product.category_name = category_name
            name = md.product.name
            unit = md.product.unit
            quantity = md.product.quantity
            exp_date = md.product.exp_date
            note = md.product.note
            category = md.product.category_name
        sm.send_message(
            templates.check_md(name, unit, quantity, exp_date, note, category),
            state=ProductCreateStatesGroup.check_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@exc_handler_decorator
@check_authentication_decorator
@BOT.callback_query_handler(state=ProductCreateStatesGroup.check_new)
def handle_product_create_check_new_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            product_data = md.product
            if a_token := md.user.access_jtw_token is None:
                return sm.send_message(main_m.something_went_wrong, finish_state=True)
        p_api = ProductsAPI(a_token)
        product = ProductOutSchema(**product_data.dict())
        p_api.post(product)
        with MainDataContextmanager(message) as md:
            md.product = None
        sm.send_message(messages.success, finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product = None
        sm.send_message(
            messages.try_again,
            state=ProductCreateStatesGroup.ask_add_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
