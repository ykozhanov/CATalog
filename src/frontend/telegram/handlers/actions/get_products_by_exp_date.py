from telebot.types import Message

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    handle_action_get_all_elements,
)
from src.frontend.telegram.handlers.messages_helper import MESSAGES_ACTION_GET_PRODUCTS_BY_EXP_DATE, MESSAGES_MAIN
from src.frontend.telegram.keyboards import KEYBOARD_LIST_ACTIONS
from src.frontend.telegram.states import ProductsStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.core.exceptions import ProductError
from . import PREFIX_PRODUCT_ELEMENT_PAGINATOR, ATTRS_FOR_TEMPLATE_PRODUCT, TEMPLATE_BUTTON_PRODUCT


@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m == KEYBOARD_LIST_ACTIONS.action_get_products_by_exp_date,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_product_by_exp_date(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    try:
        with MainDataContextmanager as md:
            if a_token := md.user.access_jtw_token:
                p_api = ProductsAPI(access_token=a_token)
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
            products = md.products = p_api.get_by()
    except ProductError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    handle_action_get_all_elements(
        message=message,
        prefix_element_paginator=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
        attrs_for_template=ATTRS_FOR_TEMPLATE_PRODUCT,
        template_button=TEMPLATE_BUTTON_PRODUCT,
        elements=products,
        text_for_paginator=MESSAGES_ACTION_GET_PRODUCTS_BY_EXP_DATE.message_for_paginator,
        text_for_paginator_empty=MESSAGES_ACTION_GET_PRODUCTS_BY_EXP_DATE.message_products_empty,
        state_paginator=ProductsStatesGroup.products,
    )
