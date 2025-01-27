from telebot.types import Message

from src.frontend.telegram.settings import BOT, ITEMS_PER_PAGE
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator
)

from src.frontend.telegram.bot.states import ProductsStatesGroup, ActionsStatesGroup
from src.frontend.telegram.bot.keyboards import KeyboardListActions
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.core.utils import PaginatorListHelper
from src.frontend.telegram.handlers.actions.get_all_products.utils import (
    PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_PRODUCT,
    TEMPLATE_BUTTON_PRODUCT,
)
from .messages import GetProductsByExpDateActionMessages

main_m = MainMessages()
messages = GetProductsByExpDateActionMessages()


@exc_handler_decorator
@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m.text == KeyboardListActions.action_get_products_by_exp_date,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_product_by_exp_date(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    with MainDataContextmanager(message) as md:
        if a_token := md.user.access_jtw_token:
            p_api = ProductsAPI(a_token)
        else:
            sm.send_message(main_m.something_went_wrong, finish_state=True)
            return
        products = md.products = p_api.get_by()


    sm = SendMessage(message)
    if products:
        ph = PaginatorListHelper(
            elements=products,
            prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            items_per_page=ITEMS_PER_PAGE,
        )
        buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_PRODUCT, template=TEMPLATE_BUTTON_PRODUCT)
        sm.send_message(
            messages.for_paginator,
            state=ProductsStatesGroup.products,
            inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
        )
    else:
        sm.send_message(messages.empty, delete_reply_keyboard=True, finish_state=True)
