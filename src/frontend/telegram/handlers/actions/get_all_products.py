from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT, ITEMS_PER_PAGE
from src.frontend.telegram.core.utils import SendMessage, PaginatorHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    handle_action_get_all_elements,
)
from src.frontend.telegram.handlers.utils.messages import MESSAGES_ACTION_GET_ALL_PRODUCTS, MESSAGES_MAIN
from src.frontend.telegram.bot.keyboards import KEYBOARD_LIST_ACTIONS, KEYBOARD_YES_OR_NO, KeyboardActionsByElement
from src.frontend.telegram.bot.states import ProductsStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.core.exceptions import ProductError
from src.frontend.telegram.handlers.actions.get_all_categories import get_all_categories
from . import (
    PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_PRODUCT,
    TEMPLATE_BUTTON_PRODUCT,
)


@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m.text == KEYBOARD_LIST_ACTIONS.action_get_all_products,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_products(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    get_all_categories(message)
    try:
        with MainDataContextmanager(message) as md:
            if a_token := md.user.access_jtw_token:
                p_api = ProductsAPI(access_token=a_token)
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
            products = md.products = p_api.get_all()
    except ProductError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    else:
        handle_action_get_all_elements(
            message=message,
            prefix_element_paginator=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_PRODUCT,
            template_button=TEMPLATE_BUTTON_PRODUCT,
            elements=products,
            text_for_paginator=MESSAGES_ACTION_GET_ALL_PRODUCTS.message_for_paginator,
            text_for_paginator_empty=MESSAGES_ACTION_GET_ALL_PRODUCTS.message_products_empty,
            state_paginator=ProductsStatesGroup.products,
            state_add_new_element=ProductsStatesGroup.ask_add_new_product,
        )

@BOT.callback_query_handler(
    func=lambda m: m.data == KEYBOARD_YES_OR_NO.callback_answer_no,
    state=ProductsStatesGroup.ask_add_new_product,
)
def handle_state_ask_add_new_product_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=MESSAGES_MAIN.message_to_help, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == PaginatorHelper.CALLBACK_PAGE,
    state=ProductsStatesGroup.products,
)
def handle_products_paginator(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        products = md.products
    ph = PaginatorHelper(
        elements=products,
        prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
        items_per_page=ITEMS_PER_PAGE,
    )
    sm = SendMessage(message)
    page = int(message.data.split("#")[1])
    buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_PRODUCT, template=TEMPLATE_BUTTON_PRODUCT, page=page)
    sm.send_message(
        text=MESSAGES_ACTION_GET_ALL_PRODUCTS.message_for_paginator,
        inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
    )


@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    state=ProductsStatesGroup.products,
)
def handle_product_element(message: CallbackQuery):
    sm = SendMessage(message)
    product_index, page = (int(e) for e in message.data.split("#") if e.isdigit())
    with MainDataContextmanager(message) as md:
        product = md.products
        categories = md.categories
    product = product[product_index]

    category_name = None
    for c in categories:
        if c.id == product.category_id:
            category_name = c.name
            break

    if category_name is not None:
        text = MESSAGES_ACTION_GET_ALL_PRODUCTS.template_message_get_list_detail_product_md(
            name=product.name,
            unit=product.unit,
            quantity=product.quantity,
            exp_date=product.exp_date,
            note=product.note,
            category=category_name,
        )
        inline_keyboard = KeyboardActionsByElement(page).get_inline_keyboard_product()
        sm.send_message(text=text, inline_keyboard=inline_keyboard)
    else:
        sm.send_message(MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
