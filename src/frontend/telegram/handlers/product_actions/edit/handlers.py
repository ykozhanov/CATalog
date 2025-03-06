from datetime import datetime

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import ProductDataclass
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo, KeyboardActionsByElement
from src.frontend.telegram.bot.states import ProductsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.api.products.schemas import ProductOutSchema
from src.frontend.telegram.handlers.actions.get_all_categories.utils import PREFIX_CATEGORY_ELEMENT_PAGINATOR
from src.frontend.telegram.handlers.actions.get_all_products.utils import get_category

from .utils import get_inline_categories
from .messages import (
    ProductUpdateActionMessages,
    ProductUpdateActionTemplates,
    MAX_LEN_UNIT,
    MAX_LEN_NAME,
    MAX_LEN_NOTE,
)
from .states import ProductUpdateStatesGroup

__all__ = ["handle_action_update_product"]

main_m = MainMessages()
messages = ProductUpdateActionMessages()
templates = ProductUpdateActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.message_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.EDIT_PREFIX,
    state=ProductsStatesGroup.products,
)
def handle_action_update_product(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    product_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        md.product = ProductDataclass()
        if products := md.products is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_product = products[product_index]

    sm.send_message(
        text=messages.ask_input_name,
        state=ProductUpdateStatesGroup.ask_input_name,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_name)
def handle_product_update_message_ask_input_name(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(messages.input_name, state=ProductUpdateStatesGroup.waiting_input_name)
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.name = md.old_product.name
        sm.send_message(
            messages.ask_input_unit,
            state=ProductUpdateStatesGroup.ask_input_unit,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_name)
def handle_product_update_waiting_input_name(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NAME:
        return sm.send_message(templates.error_max_len(MAX_LEN_NAME))
    with MainDataContextmanager(message) as md:
        md.product.name = message.text
    sm.send_message(
        text=messages.ask_input_unit,
        state=ProductUpdateStatesGroup.ask_input_unit,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_unit)
def handle_product_update_message_ask_input_unit(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(
            text=messages.input_unit,
            state=ProductUpdateStatesGroup.waiting_input_unit,
        )
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.unit = md.old_product.unit
        sm.send_message(
            text=messages.ask_input_quantity,
            state=ProductUpdateStatesGroup.ask_input_quantity,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_unit)
def handle_product_update_waiting_input_unit(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_UNIT:
        return sm.send_message(templates.error_max_len(MAX_LEN_UNIT))
    with MainDataContextmanager(message) as md:
        md.product.unit = message.text
    sm.send_message(
        text=messages.ask_input_quantity,
        state=ProductUpdateStatesGroup.ask_input_quantity,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_quantity)
def handle_product_update_message_ask_input_quantity(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(
            text=messages.input_quantity,
            state=ProductUpdateStatesGroup.waiting_input_quantity,
        )
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.quantity = md.old_product.quantity
        sm.send_message(
            text=messages.ask_input_exp_date,
            state=ProductUpdateStatesGroup.ask_input_exp_date,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_quantity)
def handle_product_update_waiting_input_quantity(message: Message):
    sm = SendMessage(message)
    try:
        quantity = float(message.text.replace(",", "."))
    except ValueError:
        sm.send_message(messages.error_quantity)
    else:
        with MainDataContextmanager(message) as md:
            md.product.quantity = quantity
        sm.send_message(
            text=messages.ask_input_exp_date,
            state=ProductUpdateStatesGroup.ask_input_exp_date,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_exp_date)
def handle_product_update_ask_input_exp_date(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(
            text=messages.input_day,
            state=ProductUpdateStatesGroup.waiting_input_day,
        )
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.exp_date = md.old_product.exp_date
        sm.send_message(
            text=messages.ask_input_note,
            state=ProductUpdateStatesGroup.ask_input_note,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_day)
def handle_product_update_waiting_input_day(message: Message):
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
            state=ProductUpdateStatesGroup.waiting_input_month,
        )

@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_month)
def handle_product_update_waiting_input_month(message: Message):
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
            state=ProductUpdateStatesGroup.waiting_input_year,
        )


@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_year)
def handle_product_update_waiting_input_year(message: Message):
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
            state=ProductUpdateStatesGroup.ask_input_note,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )


@check_authentication_decorator
@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_note)
def handle_product_update_ask_input_note(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        sm.send_message(
            text=messages.input_note,
            state=ProductUpdateStatesGroup.waiting_input_note,
        )
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.note = md.old_product.note
        sm.send_message(
            text=messages.ask_choice_category,
            state=ProductUpdateStatesGroup.ask_choice_category,
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@check_authentication_decorator
@telegram_bot.message_handler(state=ProductUpdateStatesGroup.waiting_input_note)
def handle_product_update_waiting_input_note(message: Message):
    sm = SendMessage(message)
    if len(message.text) > MAX_LEN_NOTE:
        return sm.send_message(templates.error_max_len(MAX_LEN_NOTE))
    with MainDataContextmanager(message) as md:
        md.product.note = message.text
    sm.send_message(
        text=messages.ask_choice_category,
        state=ProductUpdateStatesGroup.ask_choice_category,
    )


@exc_handler_decorator
@check_authentication_decorator
@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_choice_category)
def handle_product_update_ask_choice_category(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        inline_keyboard = get_inline_categories(message)

        sm.send_message(
            text=messages.choice_category,
            state=ProductUpdateStatesGroup.waiting_choice_category,
            inline_keyboard=inline_keyboard,
        )
    elif message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            categories = md.categories
            category_id = md.old_product.category_id
            if category := get_category(categories, category_id) is None:
                sm.send_message(main_m.something_went_wrong, finish_state=True)
                return
            md.product.category_id = category.id
            md.product.category_name = category.name
            name = md.product.name
            unit = md.product.unit
            quantity = md.product.quantity
            exp_date = md.product.exp_date
            note = md.product.note
            category = md.product.category_name
        sm.send_message(
            text=templates.check_md(name, unit, quantity, exp_date, note, category),
            state=ProductUpdateStatesGroup.check_update_product,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.waiting_choice_category)
def handle_product_update_waiting_category(message: CallbackQuery):
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
            state=ProductUpdateStatesGroup.check_update_product,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@exc_handler_decorator
@check_authentication_decorator
@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.check_update_product)
def handle_product_update_check_update_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            product_id = md.old_product.id
            product_data = md.product
            if a_token := md.user.access_jtw_token is None:
                return sm.send_message(main_m.something_went_wrong, finish_state=True)
        p_api = ProductsAPI(a_token)
        product = ProductOutSchema(**product_data.dict())
        p_api.put(product_id, product)
        with MainDataContextmanager(message) as md:
            md.product = None
            md.old_product = None
        sm.send_message(messages.success, finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(
            text=messages.try_again,
            state=ProductUpdateStatesGroup.ask_try_again,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)


@telegram_bot.callback_query_handler(state=ProductUpdateStatesGroup.ask_try_again)
def handle_product_update_ask_try_again(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == y_or_n.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.product = ProductDataclass()
        sm.send_message(
            text=messages.ask_input_name,
            state=ProductUpdateStatesGroup.ask_input_name,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(main_m.to_help, finish_state=True)
    else:
        sm.send_message(text=main_m.something_went_wrong, finish_state=True)
