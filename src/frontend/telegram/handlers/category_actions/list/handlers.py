from telebot.types import CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    check_authentication_decorator,
    exc_handler_decorator,
    get_inline_paginator_list,
)
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

main_m = MainMessages()
templates = CategoryListActionTemplates()
y_or_n = KeyboardYesOrNo()


@exc_handler_decorator
@check_authentication_decorator
@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == KeyboardActionsByElement.LIST_PREFIX,
    state=CategoriesStatesGroup.categories,
)
def handle_category_list_action(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.delete_message()
    category_index = int(message.data.split("#")[1])
    with MainDataContextmanager(message) as md:
        a_token = md.user.access_jtw_token
        categories = md.categories
        if categories is None or a_token is None:
            return sm.send_message(main_m.something_went_wrong, finish_state=True)
        category = categories[category_index]
        md.product.category_id = category_id = category.id
        md.product.category_name = name = category.name

    p_api = ProductsAPI(a_token)
    products = p_api.get_by(category_id=category_id)
    if products:
        inline_keyboard = get_inline_paginator_list(
            elements=products,
            prefix_element=PREFIX_PRODUCT_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_PRODUCT,
            template=TEMPLATE_BUTTON_PRODUCT,
        )
        sm.send_message(templates.list_md(name), state=ProductsStatesGroup.products, inline_keyboard=inline_keyboard)
    else:
        sm.send_message(
            text=templates.empty_md(name),
            state=ProductCreateStatesGroup.ask_add_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            delete_reply_keyboard=True,
        )
