from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.bot.states import ProductsStatesGroup
from src.frontend.telegram.bot.keyboards import KeyboardActionsByElement
from src.frontend.telegram.handlers.utils import (
    MainMessages,
    MainDataContextmanager,
    exc_handler_decorator,
    check_authentication_decorator,
)
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.api import ProductsAPI

from .messages import ProductUseActionTemplates, ProductUseActionMessages
from .states import ProductUseStatesGroup

main_m = MainMessages()
messages = ProductUseActionMessages()
templates = ProductUseActionTemplates()


@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.USE_PREFIX,
    state=ProductsStatesGroup.products,
)
def handler_product_use_action(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    product_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        if products := md.products is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.old_product = old_product = products[product_index]
    sm.send_message(
        templates.old_md(name=old_product.name, unit=old_product.unit, quantity=old_product.quantity),
        parse_mode="Markdown",
        state=ProductUseStatesGroup.input_diff,
    )


@exc_handler_decorator
@check_authentication_decorator
@BOT.message_handler(state=ProductUseStatesGroup.input_diff)
def handle_product_use_input_diff(message: Message) -> None:
    sm = SendMessage(message)
    with MainDataContextmanager(message) as md:
        old_product = md.old_product
        a_token = md.user.access_jtw_token
        md.old_product = None
    if old_product is None or a_token is None:
        return sm.send_message(main_m.something_went_wrong)
    try:
        diff = float(message.text)
    except ValueError:
        return sm.send_message(messages.error_diff)
    if diff > old_product.quantity:
        return sm.send_message(templates.error_diff(old_product.quantity))

    new_quantity = old_product.quantity - diff
    new_product = old_product
    new_product.quantity = new_quantity

    p_api = ProductsAPI(a_token)
    p_api.put(old_product.id, new_product)

    if new_quantity <= 0:
        return sm.send_message(templates.delete_md(new_product.name), parse_mode="Markdown", finish_state=True)

    sm.send_message(
        templates.new_md(new_product.name, new_product.unit, new_product.quantity),
        parse_mode="Markdown",
        finish_state=True,
    )
