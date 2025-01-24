from datetime import datetime

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage, PaginatorHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
)
from src.frontend.telegram.handlers.utils.messages import MESSAGES_ACTION_PRODUCT_CREATE, MESSAGES_MAIN
from src.frontend.telegram.bot.keyboards import KEYBOARD_YES_OR_NO
from src.frontend.telegram.bot.states import ProductsStatesGroup, ProductCreateStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.api.products.schemas import ProductOutSchema
from src.frontend.telegram.core.exceptions import ProductError, CategoryError
from src.frontend.telegram.handlers.actions import PREFIX_CATEGORY_ELEMENT_PAGINATOR
from src.frontend.telegram.handlers.actions.get_all_categories import get_all_categories


def get_inline_categories(message: Message | CallbackQuery) -> list[tuple[str, str]]:
    categories = get_all_categories(message)
    return [(c.name, f"{PREFIX_CATEGORY_ELEMENT_PAGINATOR}#{c.id}#{c.name}") for c in categories]


@BOT.callback_query_handler(
    func=lambda m: m.data == PaginatorHelper.CALLBACK_CREATE,
    state=ProductsStatesGroup.products,
)
def handle_paginator_create_new_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_name,
        state=ProductCreateStatesGroup.waiting_input_name,
    )


@BOT.callback_query_handler(state=ProductsStatesGroup.ask_add_new_product)
def handle_ask_add_new_product(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_name,
            state=ProductCreateStatesGroup.waiting_input_name,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(text=MESSAGES_MAIN.message_to_help, finish_state=True)
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_name)
def handle_product_create_waiting_input_name(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.name = message.text
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_unit,
        state=ProductCreateStatesGroup.waiting_input_unit,
    )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_unit)
def handle_product_create_waiting_input_unit(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.unit = message.text
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_quantity,
        state=ProductCreateStatesGroup.waiting_input_quantity,
    )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_quantity)
def handle_product_create_waiting_input_quantity(message: Message):
    sm = SendMessage(message)
    try:
        quantity = float(message.text)
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_CREATE.message_error_quantity)
    else:
        with MainDataContextmanager(message) as md:
            md.product.quantity = quantity
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_quantity,
            state=ProductCreateStatesGroup.ask_input_exp_date,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )


@BOT.callback_query_handler(state=ProductCreateStatesGroup.ask_input_exp_date)
def handle_product_create_ask_input_exp_date(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_day,
            state=ProductCreateStatesGroup.waiting_input_day,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_ask_note,
            state=ProductCreateStatesGroup.ask_input_note,
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_day)
def handle_product_create_waiting_input_day(message: Message):
    sm = SendMessage(message)
    try:
        day = int(message.text)
        if 31 < day < 1:
            raise ValueError
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_CREATE.message_error_day)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_day = day
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_month,
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
        sm.send_message(MESSAGES_ACTION_PRODUCT_CREATE.message_error_month)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_month = month
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_year,
            state=ProductCreateStatesGroup.waiting_input_year,
        )


@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_year)
def handle_product_create_waiting_input_year(message: Message):
    sm = SendMessage(message)
    try:
        year = datetime.strptime(message.text, "%y").year
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_CREATE.message_error_year)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_year = year
            exp_date = datetime(year, month=md.product.exp_date_month, day=md.product.exp_date_day).date()
            md.product.exp_date = exp_date
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_ask_note,
            state=ProductCreateStatesGroup.ask_input_note,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductCreateStatesGroup.ask_input_note)
def handle_product_create_ask_input_note(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_input_note,
            state=ProductCreateStatesGroup.waiting_input_note,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        try:
            inline_keyboard = get_inline_categories(message)
        except CategoryError as e:
            sm.send_message(MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
        else:
            sm.send_message(
                text=MESSAGES_ACTION_PRODUCT_CREATE.message_choice_category,
                state=ProductCreateStatesGroup.waiting_category,
                inline_keyboard=inline_keyboard,
            )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@check_authentication_decorator
@BOT.message_handler(state=ProductCreateStatesGroup.waiting_input_note)
def handle_product_create_waiting_input_note(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.note = message.text
    try:
        inline_keyboard = get_inline_categories(message)
    except CategoryError as e:
        sm.send_message(MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    else:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_choice_category,
            state=ProductCreateStatesGroup.waiting_category,
            inline_keyboard=inline_keyboard,
        )


@BOT.callback_query_handler(state=ProductCreateStatesGroup.waiting_category)
def handle_product_create_waiting_category(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data.split("#")[0] == PREFIX_CATEGORY_ELEMENT_PAGINATOR:
        with MainDataContextmanager(message) as md:
            md.product.category_id = int(message.data.split("#")[1])
            md.product.category_name = message.data.split("#")[2]
            name = md.product.name
            unit = md.product.unit
            quantity = md.product.quantity
            exp_date = md.product.exp_date
            note = md.product.note
            category = md.product.category_name
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.template_message_check(name, unit, quantity, exp_date, note, category),
            state=ProductCreateStatesGroup.check_new_product,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductCreateStatesGroup.check_new_product)
def handle_product_create_check_new_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            p_api = ProductsAPI(md.user.access_jtw_token)
            product = ProductOutSchema(**md.product.dict())
        try:
            p_api.post(product)
        except ProductError as e:
            sm.send_message(MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
        else:
            with MainDataContextmanager(message) as md:
                md.product = None
            sm.send_message(text=MESSAGES_ACTION_PRODUCT_CREATE.message_success_create, finish_state=True)
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_CREATE.message_try_again,
            state=ProductCreateStatesGroup.ask_add_new_product,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
