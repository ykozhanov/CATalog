from telebot.types import CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.bot.states import ProductsStatesGroup
from src.frontend.telegram.bot.keyboards import KeyboardActionsByElement, KeyboardYesOrNo
from src.frontend.telegram.handlers.utils import (
    MainMessages,
    MainDataContextmanager,
    exc_handler_decorator,
    check_authentication_decorator,
)
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.api import ProductsAPI

from .messages import ProductDeleteActionTemplates
from .states import ProductDeleteStatesGroup

main_m = MainMessages()
templates = ProductDeleteActionTemplates()
y_or_n = KeyboardYesOrNo()


@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.DELETE_PREFIX,
    state=ProductsStatesGroup.products,
)
def handler_product_delete_action(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    product_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        if products := md.products is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_product = old_product = products[product_index]
    sm.send_message(
        templates.confirm_md(old_product.name),
        parse_mode="Markdown",
        state=ProductDeleteStatesGroup.confirm_delete,
        inline_keyboard=y_or_n.get_inline_keyboard(),
    )


@exc_handler_decorator
@check_authentication_decorator
@BOT.callback_query_handler(state=ProductDeleteStatesGroup.confirm_delete)
def handle_product_delete_confirm_delete(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    with MainDataContextmanager(message) as md:
        old_product = md.old_product
        a_token = md.user.access_jtw_token
        md.old_product = None
    if message.data == y_or_n.callback_answer_yes:
        if old_product is None or a_token is None:
            return sm.send_message(main_m.something_went_wrong)
        p_api = ProductsAPI(a_token)
        p_api.delete(old_product.id)
        sm.send_message(templates.success_md(old_product.name), parse_mode="Markdown", finish_state=True)
    elif message.data == y_or_n.callback_answer_no:
        sm.send_message(templates.answer_no_md(old_product.name), parse_mode="Markdown", finish_state=True)
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
