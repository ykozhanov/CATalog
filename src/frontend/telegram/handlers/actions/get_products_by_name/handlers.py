from telebot.types import Message

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
    get_inline_paginator_list,
)
from src.frontend.telegram.bot.keyboards import k_list_actions
from src.frontend.telegram.bot.states import ProductsStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.handlers.actions.get_all_products.utils import (
    PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_PRODUCT,
    TEMPLATE_BUTTON_PRODUCT,
)
from .messages import GetProductsByNameActionMessages, GetProductsByNameActionTemplates

__all__ = ["handle_action_get_product_by_name"]


main_m = MainMessages()
messages = GetProductsByNameActionMessages()
templates = GetProductsByNameActionTemplates()


@telegram_bot.message_handler(
    func=lambda m: m.text == k_list_actions.action_get_product_by_name,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_product_by_name(message: Message) -> None:
    sm = SendMessage(message)
    sm.send_message(
        messages.input_name,
        state=ProductsStatesGroup.waiting_name_product,
        delete_reply_keyboard=True,
    )


@exc_handler_decorator
@check_authentication_decorator
@telegram_bot.message_handler(state=ProductsStatesGroup.waiting_name_product)
def handle_name_product_for_get_product_by_name(message: Message) -> None:
    sm = SendMessage(message)
    name = message.text

    with MainDataContextmanager(message) as md:
        if a_token := md.user.access_jtw_token is None:
            return sm.send_message(
                main_m.something_went_wrong,
                finish_state=True,
                delete_reply_keyboard=True,
            )
        p_api = ProductsAPI(access_token=a_token)
        products = md.products = p_api.get_by(name=name)
    if products:
        inline_keyboard = get_inline_paginator_list(
            elements=products,
            prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_PRODUCT,
            template=TEMPLATE_BUTTON_PRODUCT,
        )
        sm.send_message(
            templates.for_paginator(name),
            state=ProductsStatesGroup.products,
            inline_keyboard=inline_keyboard,
            delete_reply_keyboard=True,
        )
    else:
        sm.send_message(templates.empty(name), delete_reply_keyboard=True, finish_state=True)
