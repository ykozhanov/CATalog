from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT, ITEMS_PER_PAGE
from src.frontend.telegram.core.utils import SendMessage, PaginatorListHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    exc_handler_decorator,
    check_authentication_decorator,
)
from src.frontend.telegram.bot.keyboards import KeyboardListActions, KeyboardYesOrNo, KeyboardActionsByElement
from src.frontend.telegram.bot.states import ActionsStatesGroup, ProductsStatesGroup
from src.frontend.telegram.api import ProductsAPI
from src.frontend.telegram.handlers.actions.get_all_categories.utils import get_all_categories

from .messages import GetAllProductsActionMessages, GetAllProductsActionTemplates
from .utils import (
    get_category,
    PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_PRODUCT,
    TEMPLATE_BUTTON_PRODUCT,
)

main_m = MainMessages()
messages = GetAllProductsActionMessages()
templates = GetAllProductsActionTemplates()
y_or_n = KeyboardYesOrNo()


@exc_handler_decorator
@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m.text == KeyboardListActions.action_get_all_products,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_products(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    get_all_categories(message)
    with MainDataContextmanager(message) as md:
        if a_token := md.user.access_jtw_token:
            p_api = ProductsAPI(access_token=a_token)
        else:
            sm.send_message(text=main_m.something_went_wrong, finish_state=True)
            return
        products = md.products = p_api.get_all()
    if products:
        ph = PaginatorListHelper(
            elements=products,
            prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            items_per_page=ITEMS_PER_PAGE,
        )
        buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_PRODUCT, template=TEMPLATE_BUTTON_PRODUCT)
        sm.send_message(
            text=messages.for_paginator,
            state=ProductsStatesGroup.products,
            inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
        )
    else:
        sm.send_message(
            text=messages.empty,
            state=ProductsStatesGroup.ask_add_new_product,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            delete_reply_keyboard=True,
        )


@BOT.callback_query_handler(
    func=lambda m: m.data == y_or_n.callback_answer_no,
    state=ProductsStatesGroup.ask_add_new_product,
)
def handle_state_ask_add_new_product_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=main_m.to_help, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == PaginatorListHelper.CALLBACK_PAGE,
    state=ProductsStatesGroup.products,
)
def handle_products_paginator(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        products = md.products
    ph = PaginatorListHelper(
        elements=products,
        prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
        items_per_page=ITEMS_PER_PAGE,
    )
    sm = SendMessage(message)
    page = int(message.data.split("#")[1])
    buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_PRODUCT, template=TEMPLATE_BUTTON_PRODUCT, page=page)
    sm.send_message(
        text=messages.for_paginator,
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
    category = get_category(categories, product.category_id)
    if category is not None:
        text = templates.detail_md(
            name=product.name,
            unit=product.unit,
            quantity=product.quantity,
            exp_date=product.exp_date,
            note=product.note,
            category=category.name,
        )
        inline_keyboard = KeyboardActionsByElement(page, product_index).get_inline_keyboard_product()
        sm.send_message(text=text, inline_keyboard=inline_keyboard, parse_mode="Markdown")
    else:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
