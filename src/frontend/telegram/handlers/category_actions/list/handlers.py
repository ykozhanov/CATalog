import logging

from telebot.types import CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
    get_inline_paginator_list, escape_markdown,
)
from src.frontend.telegram.handlers.utils.md_dataclasses import ProductDataclass
from src.frontend.telegram.bot.keyboards import KeyboardActionsByElement, KeyboardYesOrNo
from src.frontend.telegram.bot.states import CategoriesStatesGroup, ProductsStatesGroup
from src.frontend.telegram.handlers.product_actions.create.states import ProductCreateStatesGroup
from src.frontend.telegram.handlers.actions.get_all_products.utils import (
    PREFIX_PRODUCT_ELEMENT_PAGINATOR,
    TEMPLATE_BUTTON_PRODUCT,
    ATTRS_FOR_TEMPLATE_PRODUCT,
)
from src.frontend.telegram.api import ProductsAPI

from .messages import CategoryListActionTemplates

__all__ = ["handle_category_list_action"]

main_m = MainMessages()
templates = CategoryListActionTemplates()
y_or_n = KeyboardYesOrNo()


@telegram_bot.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.LIST_PREFIX,
    state=CategoriesStatesGroup.categories,
)
@exc_handler_decorator
@check_authentication_decorator
def handle_category_list_action(message: CallbackQuery) -> None:
    logging.info(f"Старт 'handle_category_list_action'")
    sm = SendMessage(message)
    sm.delete_message()
    category_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        a_token = md.user.access_jtw_token
        categories = md.categories
        if categories is None or a_token is None:
            logging.info(f"Конец 'handle_category_list_action'")
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        md.product = ProductDataclass()
        md.product.category_id = category_id = categories[category_index].id
        md.product.category_name = name = categories[category_index].name
        p_api = ProductsAPI(a_token)
        products = md.products = p_api.get_by(category_id=category_id)
    logging.debug(f"products: {products}")
    logging.debug(f"md.products: {md.products}")
    if products:
        inline_keyboard = get_inline_paginator_list(
            elements=products,
            prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_PRODUCT,
            template=TEMPLATE_BUTTON_PRODUCT,
        )
        sm.send_message(
            templates.list_md(escape_markdown(name)),
            state=ProductsStatesGroup.products,
            inline_keyboard=inline_keyboard,
            parse_mode="Markdown"
        )
    else:
        sm.send_message(
            templates.empty_md(escape_markdown(name)),
            state=ProductCreateStatesGroup.ask_add_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            parse_mode="Markdown",
        )
    logging.info(f"Конец 'handle_category_list_action'")
