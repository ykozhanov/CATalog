import logging
from datetime import datetime

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage, PaginatorListHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
    escape_markdown,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import ProductDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo
from src.frontend.telegram.bot.states import ProductsStatesGroup, CategoriesStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.api.products.exceptions import ProductError
from src.frontend.telegram.api.products.exceptions import MESSAGE_PRODUCT_ERROR
from src.frontend.telegram.api.products.schemas import ProductOutSchema
from src.frontend.telegram.handlers.actions.get_all_categories.utils import PREFIX_CATEGORY_ELEMENT_PAGINATOR
from .messages import (
    ProductCreateActionMessages,
    ProductCreateActionTemplates,
    MAX_LEN_NOTE,
    MAX_LEN_UNIT,
    MAX_LEN_NAME,
)
from .utils import get_inline_categories, year_str_to_int, day_str_to_int, month_str_to_int
from .states import ProductCreateStatesGroup

__all__ = ["handle_paginator_create_new_product"]

main_m = MainMessages()
messages = ProductCreateActionMessages()
templates = ProductCreateActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.callback_query_handler(
    func=lambda m: m.data == PaginatorListHelper.CALLBACK_CREATE,
    state=ProductsStatesGroup.products,
)
@exc_handler_decorator
@check_authentication_decorator
def handle_paginator_create_new_product(message: CallbackQuery):
    logging.info(f"Старт 'handle_paginator_create_new_product'")
    sm = SendMessage(message)
    sm.delete_message()
    logging.debug(f"user_id: {sm.msg_data.user_id}, chat_id: {sm.msg_data.chat_id}")
    categories = get_inline_categories(message)
    with MainDataContextmanager(message) as md:
        md.product = ProductDataclass()
        md.product.list_categories = categories
        logging.debug(f"md.product: {md.product}")
    logging.debug(f"categories: {categories}")
    if not categories:
        create_category_btn = [(PaginatorListHelper.CREATE_TEXT, PaginatorListHelper.CALLBACK_CREATE)]
        logging.info(f"Конец 'handle_paginator_create_new_product'")
        return sm.send_message(
            messages.not_categories,
            state=CategoriesStatesGroup.categories,
            inline_keyboard=create_category_btn,
        )
    sm.send_message(messages.input_name, state=ProductCreateStatesGroup.waiting_input_name)
    logging.info(f"Конец 'handle_paginator_create_new_product'")


@telegram_bot.callback_query_handler(state=ProductCreateStatesGroup.ask_add_new)
@exc_handler_decorator
@check_authentication_decorator
def handle_ask_add_new_product(message: CallbackQuery) -> None:
    logging.info(f"Старт 'handle_ask_add_new_product'")
    sm = SendMessage(message)
    sm.delete_message()
    logging.debug(f"user_id: {sm.msg_data.user_id}, chat_id: {sm.msg_data.chat_id}")
    if message.data == y_or_n.callback_answer_yes:
        categories = get_inline_categories(message)
        with MainDataContextmanager(message) as md:
            md.product = ProductDataclass()
            md.product.list_categories = categories
            logging.debug(f"md.product: {md.product}")
        logging.debug(f"categories: {categories}")
        if not categories:
            create_category_btn = [(PaginatorListHelper.CREATE_TEXT, PaginatorListHelper.CALLBACK_CREATE)]
            logging.info(f"Конец 'handle_ask_add_new_product'")
            return sm.send_message(
                messages.not_categories,
                state=CategoriesStatesGroup.categories,
                inline_keyboard=create_category_btn,
            )
        sm.send_message(messages.input_name, state=ProductCreateStatesGroup.waiting_input_name)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(main_m.to_help, finish_state=True)
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
    logging.info(f"Конец 'handle_ask_add_new_product'")


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_name)
def handle_product_create_waiting_input_name(message: Message):
    logging.info(f"Старт 'handle_product_create_waiting_input_name'")
    sm = SendMessage(message)
    logging.debug(f"user_id: {sm.msg_data.user_id}, chat_id: {sm.msg_data.chat_id}")
    if len(message.text) > MAX_LEN_NAME:
        logging.info(f"Конец 'handle_product_create_waiting_input_name'")
        return sm.send_message(templates.error_max_len(MAX_LEN_NAME))
    with MainDataContextmanager(message) as md:
        md.product.name = message.text
        logging.debug(f"md.product: {md.product}")
    sm.send_message(messages.input_unit, state=ProductCreateStatesGroup.waiting_input_unit)
    logging.info(f"Конец 'handle_product_create_waiting_input_name'")


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_unit)
def handle_product_create_waiting_input_unit(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_UNIT:
        return sm.send_message(templates.error_max_len(MAX_LEN_UNIT))
    with MainDataContextmanager(message) as md:
        md.product.unit = message.text
    sm.send_message(messages.input_quantity, state=ProductCreateStatesGroup.waiting_input_quantity)


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_quantity)
def handle_product_create_waiting_input_quantity(message: Message):
    sm = SendMessage(message)
    try:
        if (quantity := float(message.text.replace(",", "."))) <= 0:
            raise ValueError()
    except ValueError:
        return sm.send_message(messages.error_quantity)
    else:
        with MainDataContextmanager(message) as md:
            md.product.quantity = quantity
        sm.send_message(
            messages.ask_input_exp_date,
            state=ProductCreateStatesGroup.ask_input_exp_date,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )


@telegram_bot.callback_query_handler(state=ProductCreateStatesGroup.ask_input_exp_date)
def handle_product_create_ask_input_exp_date(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_day, state=ProductCreateStatesGroup.waiting_input_day)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(
            text=messages.ask_input_note,
            state=ProductCreateStatesGroup.ask_input_note,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_day)
def handle_product_create_waiting_input_day(message: Message):
    sm = SendMessage(message)
    try:
        day = day_str_to_int(message.text)
    except ValueError:
        sm.send_message(messages.error_day)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_day = day
        sm.send_message(messages.input_month, state=ProductCreateStatesGroup.waiting_input_month)

@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_month)
def handle_product_create_waiting_input_month(message: Message):
    sm = SendMessage(message)
    try:
        month = month_str_to_int(message.text)
    except ValueError:
        sm.send_message(messages.error_month)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_month = month
        sm.send_message(messages.input_year, state=ProductCreateStatesGroup.waiting_input_year)


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_year)
@exc_handler_decorator
def handle_product_create_waiting_input_year(message: Message):
    logging.info(f"Старт 'handle_product_create_waiting_input_year'")
    sm = SendMessage(message)
    try:
        year = year_str_to_int(message.text)
    except ValueError:
        logging.info(f"Конец 'handle_product_create_waiting_input_year'")
        return sm.send_message(messages.error_year)
    else:
        with MainDataContextmanager(message) as md:
            logging.debug(f"md.product: {md.product}")
            md.product.exp_date_year = year
            day = md.product.exp_date_day
            month = md.product.exp_date_month
            logging.debug(f"types: year - {type(year)}, month - {type(month)}, day - {type(day)}")
            try:
                exp_date = datetime(year=year, month=month, day=day).date()
            except ValueError:
                raise ProductError(f"{MESSAGE_PRODUCT_ERROR}: Не верная дата {day}.{month}.{year}")
            md.product.exp_date = exp_date
        sm.send_message(
            text=messages.ask_input_note,
            state=ProductCreateStatesGroup.ask_input_note,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
        logging.info(f"Конец 'handle_product_create_waiting_input_year'")


@telegram_bot.callback_query_handler(state=ProductCreateStatesGroup.ask_input_note)
@exc_handler_decorator
@check_authentication_decorator
def handle_product_create_ask_input_note(message: CallbackQuery):
    logging.info(f"Старт 'handle_product_create_ask_input_note'")
    sm = SendMessage(message)
    sm.delete_message()
    with MainDataContextmanager(message) as md:
        logging.debug(f"md.product: {md.product}")
        categories = md.product.list_categories
        logging.debug(f"md.product.list_categories: {md.product.list_categories}")
    if categories is None:
        logging.debug(f"categories: {categories}")
        logging.info(f"Конец 'handle_product_create_ask_input_note'")
        return sm.send_message(main_m.something_went_wrong, finish_state=True)
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_note, state=ProductCreateStatesGroup.waiting_input_note)
    elif message.data == y_or_n.callback_answer_no:
        inline_keyboard = categories
        sm.send_message(
            text=messages.choice_category,
            state=ProductCreateStatesGroup.waiting_choice_category,
            inline_keyboard=inline_keyboard,
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)
    logging.info(f"Конец 'handle_product_create_ask_input_note'")


@telegram_bot.message_handler(state=ProductCreateStatesGroup.waiting_input_note)
@exc_handler_decorator
@check_authentication_decorator
def handle_product_create_waiting_input_note(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NOTE:
        return sm.send_message(templates.error_max_len(MAX_LEN_NOTE))
    with MainDataContextmanager(message) as md:
        md.product.note = message.text
        category_id = md.product.category_id
        category_name = md.product.category_name
        categories = md.product.list_categories
    if categories is None:
        return sm.send_message(main_m.something_went_wrong, finish_state=True)
    inline_keyboard = categories
    if category_id is None or category_name is None:
        sm.send_message(
            messages.choice_category,
            state=ProductCreateStatesGroup.waiting_choice_category,
            inline_keyboard=inline_keyboard,
        )
    else:
        with MainDataContextmanager(message) as md:
            text = templates.check_md(
                    name=escape_markdown(md.product.name),
                    unit=escape_markdown(md.product.unit),
                    quantity=md.product.quantity,
                    exp_date=md.product.exp_date,
                    note=escape_markdown(md.product.note) if md.product.note is not None else md.product.note,
                    category=escape_markdown(md.product.category_name),
                )
        sm.send_message(
            text,
            state=ProductCreateStatesGroup.check_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )


@telegram_bot.callback_query_handler(state=ProductCreateStatesGroup.waiting_choice_category)
def handle_product_create_waiting_category(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data.split("#")[0] == PREFIX_CATEGORY_ELEMENT_PAGINATOR:
        category_id, category_name = message.data.split("#")[1:]
        with MainDataContextmanager(message) as md:
            md.product.category_id = category_id
            md.product.category_name = category_name
            text = templates.check_md(
                name=escape_markdown(md.product.name),
                unit=escape_markdown(md.product.unit),
                quantity=md.product.quantity,
                exp_date=md.product.exp_date,
                note=escape_markdown(md.product.note) if md.product.note is not None else md.product.note,
                category=escape_markdown(md.product.category_name),
            )
        sm.send_message(
            text,
            state=ProductCreateStatesGroup.check_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.callback_query_handler(state=ProductCreateStatesGroup.check_new)
@exc_handler_decorator
@check_authentication_decorator
def handle_product_create_check_new_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            product_data = md.product
            a_token = md.user.access_jtw_token
        if a_token is None:
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
