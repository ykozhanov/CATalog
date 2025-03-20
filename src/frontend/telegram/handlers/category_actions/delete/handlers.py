from telebot.types import CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.bot.states import CategoriesStatesGroup
from src.frontend.telegram.bot.keyboards import KeyboardActionsByElement, KeyboardYesOrNo
from src.frontend.telegram.handlers.utils import (
    MainMessages,
    MainDataContextmanager,
    exc_handler_decorator,
    check_authentication_decorator, escape_markdown,
)
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.api import CategoriesAPI

from .messages import CategoryDeleteActionTemplates, CategoryDeleteActionMessages
from .states import CategoryDeleteStatesGroup

__all__ = ["handler_category_delete_action"]

main_m = MainMessages()
messages = CategoryDeleteActionMessages()
templates = CategoryDeleteActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.DELETE_PREFIX,
    state=CategoriesStatesGroup.categories,
)
def handler_category_delete_action(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    category_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        categories = md.categories
        if categories is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_category = categories[category_index]
    sm.send_message(
        messages.ask_delete_products,
        state=CategoryDeleteStatesGroup.ask_delete_products,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@telegram_bot.callback_query_handler(state=CategoryDeleteStatesGroup.ask_delete_products)
def handle_category_delete_ask_delete_products(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    delete_all_products = message.data == y_or_n.callback_answer_yes
    if message.data == y_or_n.callback_answer_yes or message.data == y_or_n.callback_answer_no:
        with MainDataContextmanager(message) as md:
            old_category = md.old_category
            md.category.delete_all_products = delete_all_products
            if old_category is None:
                return sm.send_message(main_m.something_went_wrong, finish_state=True)
        name = old_category.name
        text = templates.confirm_all_md(escape_markdown(name)) if delete_all_products \
            else templates.confirm_only_category_md(escape_markdown(name))
        sm.send_message(
            text,
            parse_mode="Markdown",
            inline_keyboard=y_or_n.get_inline_keyboard(),
            state=CategoryDeleteStatesGroup.confirm_delete,
        )
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)

@telegram_bot.callback_query_handler(state=CategoryDeleteStatesGroup.confirm_delete)
@exc_handler_decorator
@check_authentication_decorator
def handle_product_delete_confirm_delete(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        old_category = md.old_category
        a_token = md.user.access_jtw_token
        delete_all_products = md.category.delete_all_products
    check_args = [old_category, a_token, delete_all_products]
    if message.data == y_or_n.callback_answer_yes:
        if all(arg is None for arg in check_args):
            return sm.send_message(main_m.something_went_wrong)
        c_api = CategoriesAPI(a_token)
        c_api.delete(old_category.id, delete_all_products)
        text = templates.success_md(escape_markdown(old_category.name))
        sm.send_message(text, parse_mode="Markdown", finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        text = templates.answer_no_md(escape_markdown(old_category.name))
        sm.send_message(text, parse_mode="Markdown", finish_state=True)
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
        