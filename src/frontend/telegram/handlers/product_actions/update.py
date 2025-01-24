from datetime import datetime

from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
)
from src.frontend.telegram.handlers.utils.messages import MESSAGES_ACTION_PRODUCT_UPDATE, MESSAGES_MAIN
from src.frontend.telegram.handlers.utils.md_dataclasses import ProductDataclass
from src.frontend.telegram.bot.keyboards import KEYBOARD_YES_OR_NO, KeyboardActionsByElement
from src.frontend.telegram.bot.states import ProductsStatesGroup, ProductUpdateStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.api.products.schemas import ProductOutSchema
from src.frontend.telegram.api.categories.schemas import CategoryInSchema
from src.frontend.telegram.core.exceptions import ProductError, CategoryError
from src.frontend.telegram.handlers.actions import PREFIX_CATEGORY_ELEMENT_PAGINATOR
from src.frontend.telegram.handlers.actions.get_all_categories import get_all_categories


def get_inline_categories(message: Message | CallbackQuery) -> list[tuple[str, str]]:
    categories = get_all_categories(message)
    return [(c.name, f"{PREFIX_CATEGORY_ELEMENT_PAGINATOR}#{c.id}#{c.name}") for c in categories]


def get_category_by_old(message: Message | CallbackQuery) -> CategoryInSchema | None:
    with MainDataContextmanager(message) as md:
        categories = md.categories
        category_id = md.old_product.category_id
    category = None
    for c in categories:
        if c.id == category_id:
            category = c
            break
    return category


@BOT.message_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.UPDATE_PREFIX,
    state=ProductsStatesGroup.products,
)
def handle_action_update_product(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    product_id = int(message.text.split("#")[1])
    with MainDataContextmanager(message) as md:
        md.product = ProductDataclass()
        if products := md.products:
            md.old_product = products[product_id]
        else:
            sm.send_message(MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_name,
        state=ProductUpdateStatesGroup.ask_input_name,
        inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
    )


@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_name)
def handle_product_update_message_ask_input_name(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_name,
            state=ProductUpdateStatesGroup.waiting_input_name,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.name = md.old_product.name
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_unit,
            state=ProductUpdateStatesGroup.ask_input_unit,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_name)
def handle_product_update_waiting_input_name(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.name = message.text
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_unit,
        state=ProductUpdateStatesGroup.ask_input_unit,
        inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
    )


@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_unit)
def handle_product_update_message_ask_input_unit(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_unit,
            state=ProductUpdateStatesGroup.waiting_input_unit,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.unit = md.old_product.unit
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_quantity,
            state=ProductUpdateStatesGroup.ask_input_quantity,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_unit)
def handle_product_update_waiting_input_unit(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.unit = message.text
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_quantity,
        state=ProductUpdateStatesGroup.ask_input_quantity,
        inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
    )


@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_quantity)
def handle_product_update_message_ask_input_quantity(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_quantity,
            state=ProductUpdateStatesGroup.waiting_input_quantity,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.quantity = md.old_product.quantity
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_exp_date,
            state=ProductUpdateStatesGroup.ask_input_exp_date,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_quantity)
def handle_product_update_waiting_input_quantity(message: Message):
    sm = SendMessage(message)
    try:
        quantity = float(message.text)
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_UPDATE.message_error_quantity)
    else:
        with MainDataContextmanager(message) as md:
            md.product.quantity = quantity
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_exp_date,
            state=ProductUpdateStatesGroup.ask_input_exp_date,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )


@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_exp_date)
def handle_product_update_ask_input_exp_date(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_day,
            state=ProductUpdateStatesGroup.waiting_input_day,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.exp_date = md.old_product.exp_date
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_note,
            state=ProductUpdateStatesGroup.ask_input_note,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_day)
def handle_product_update_waiting_input_day(message: Message):
    sm = SendMessage(message)
    try:
        day = int(message.text)
        if 31 < day < 1:
            raise ValueError
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_UPDATE.message_error_day)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_day = day
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_month,
            state=ProductUpdateStatesGroup.waiting_input_month,
        )

@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_month)
def handle_product_update_waiting_input_month(message: Message):
    sm = SendMessage(message)
    try:
        month = int(message.text)
        if 12 < month < 1:
            raise ValueError
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_UPDATE.message_error_month)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_month = month
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_year,
            state=ProductUpdateStatesGroup.waiting_input_year,
        )


@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_year)
def handle_product_update_waiting_input_year(message: Message):
    sm = SendMessage(message)
    try:
        year = datetime.strptime(message.text, "%y").year
    except ValueError:
        sm.send_message(MESSAGES_ACTION_PRODUCT_UPDATE.message_error_year)
    else:
        with MainDataContextmanager(message) as md:
            md.product.exp_date_year = year
            exp_date = datetime(year, month=md.product.exp_date_month, day=md.product.exp_date_day).date()
            md.product.exp_date = exp_date
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_note,
            state=ProductUpdateStatesGroup.ask_input_note,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_input_note)
def handle_product_update_ask_input_note(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_input_note,
            state=ProductUpdateStatesGroup.waiting_input_note,
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        with MainDataContextmanager(message) as md:
            md.product.note = md.old_product.note
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_choice_category,
            state=ProductUpdateStatesGroup.ask_choice_category,
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@check_authentication_decorator
@BOT.message_handler(state=ProductUpdateStatesGroup.waiting_input_note)
def handle_product_update_waiting_input_note(message: Message):
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        md.product.note = message.text
    sm.send_message(
        text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_choice_category,
        state=ProductUpdateStatesGroup.ask_choice_category,
    )


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_choice_category)
def handle_product_update_ask_choice_category(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        try:
            inline_keyboard = get_inline_categories(message)
        except CategoryError as e:
            sm.send_message(MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
        else:
            sm.send_message(
                text=MESSAGES_ACTION_PRODUCT_UPDATE.message_choice_category,
                state=ProductUpdateStatesGroup.waiting_choice_category,
                inline_keyboard=inline_keyboard,
            )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        category = get_category_by_old(message)
        if category is None:
            sm.send_message(MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
            return
        with MainDataContextmanager(message) as md:
            md.product.category_id = category.id
            md.product.category_name = category.name
            name = md.product.name
            unit = md.product.unit
            quantity = md.product.quantity
            exp_date = md.product.exp_date
            note = md.product.note
            category = md.product.category_name
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.template_message_check(name, unit, quantity, exp_date, note, category),
            state=ProductUpdateStatesGroup.check_update_product,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@BOT.callback_query_handler(state=ProductUpdateStatesGroup.waiting_choice_category)
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
            text=MESSAGES_ACTION_PRODUCT_UPDATE.template_message_check(name, unit, quantity, exp_date, note, category),
            state=ProductUpdateStatesGroup.check_update_product,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductUpdateStatesGroup.check_update_product)
def handle_product_update_check_update_product(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            product_id = md.old_product.id
            p_api = ProductsAPI(md.user.access_jtw_token)
            product = ProductOutSchema(**md.product.dict())
        try:
            p_api.put(product_id, product)
        except ProductError as e:
            sm.send_message(MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
        else:
            with MainDataContextmanager(message) as md:
                md.product = None
                md.old_product = None
            sm.send_message(text=MESSAGES_ACTION_PRODUCT_UPDATE.message_success_update, finish_state=True)
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_try_again,
            state=ProductUpdateStatesGroup.ask_try_again,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(state=ProductUpdateStatesGroup.ask_try_again)
def handle_product_update_ask_try_again(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    if message.data == KEYBOARD_YES_OR_NO.callback_answer_yes:
        with MainDataContextmanager(message) as md:
            md.product = ProductDataclass()
        sm.send_message(
            text=MESSAGES_ACTION_PRODUCT_UPDATE.message_ask_input_name,
            state=ProductUpdateStatesGroup.ask_input_name,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
        )
    elif message.data == KEYBOARD_YES_OR_NO.callback_answer_no:
        sm.send_message(MESSAGES_MAIN.message_to_help, finish_state=True)
    else:
        sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
