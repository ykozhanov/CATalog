from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    PaginatorHelper,
)
from src.frontend.telegram.handlers.messages_helper import MESSAGES_ACTION_GET_ALL_PRODUCTS, MESSAGES_MAIN
from src.frontend.telegram.keyboards import KEYBOARD_LIST_ACTIONS, KEYBOARD_YES_OR_NO
from src.frontend.telegram.states import ProductsStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.core.exceptions import ProductError

PREFIX_PRODUCT_ELEMENT_PAGINATOR = "product"
ph = PaginatorHelper()


@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m == KEYBOARD_LIST_ACTIONS.action_get_all_products,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_products(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    try:
        with MainDataContextmanager as md:
            if a_token := md.user.access_jtw_token:
                p_api = ProductsAPI(access_token=a_token)
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
            md.products = p_api.get_all()
            products = md.products
    except ProductError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    if products:
        product = products[0]
        text = MESSAGES_ACTION_GET_ALL_PRODUCTS.template_message_get_list_all_products_md(**product.model_dump())
        paginator = ph.get_list_paginator(page_count=len(products), prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR)
        sm.send_message(
            text,
            parse_mode="Markdown",
            state=ProductsStatesGroup.product,
            paginator_keyboard=paginator,
        )
    else:
        #TODO Добавить обработку в создание товара
        sm.send_message(
            text=MESSAGES_ACTION_GET_ALL_PRODUCTS.products_empty,
            state=ProductsStatesGroup.ask_add_new_product,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
            delete_reply_keyboard=True,
        )

@BOT.callback_query_handler(
    func=lambda m: m.data == KEYBOARD_YES_OR_NO.callback_answer_no,
    state=ProductsStatesGroup.ask_add_new_product,
)
def handle_state_ask_add_new_product_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=MESSAGES_MAIN.message_to_help, finish_state=True)
