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
from src.frontend.telegram.bot.states import ActionsStatesGroup, CategoriesStatesGroup

from .messages import GetAllCategoriesActionMessages, GetAllCategoriesActionTemplates
from .utils import (
    get_all_categories,
    PREFIX_CATEGORY_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_CATEGORY,
    TEMPLATE_BUTTON_CATEGORY,
)

main_m = MainMessages()
messages = GetAllCategoriesActionMessages()
templates = GetAllCategoriesActionTemplates()
y_or_n = KeyboardYesOrNo()


@exc_handler_decorator
@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m.text == KeyboardListActions.action_get_all_categories,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_categories(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()

    if categories := get_all_categories(message) is None:
        sm.send_message(main_m.something_went_wrong, finish_state=True)
        return

    if categories:
        ph = PaginatorListHelper(
            elements=categories,
            prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
            items_per_page=ITEMS_PER_PAGE,
        )
        buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_CATEGORY, template=TEMPLATE_BUTTON_CATEGORY)
        sm.send_message(
            text=messages.for_paginator,
            state=CategoriesStatesGroup.categories,
            inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
        )
    else:
        sm.send_message(
            text=messages.empty,
            state=CategoriesStatesGroup.ask_add_new_category,
            inline_keyboard=y_or_n.get_inline_keyboard(),
            delete_reply_keyboard=True,
        )


@BOT.callback_query_handler(
    func=lambda m: m.data == y_or_n.callback_answer_no,
    state=CategoriesStatesGroup.ask_add_new_category,
)
def handle_state_ask_add_new_category_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=main_m.to_help, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(
    func=lambda m: m.split("#")[0] == PaginatorListHelper.CALLBACK_PAGE,
    state=CategoriesStatesGroup.categories,
)
def handle_categories_paginator(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        categories = md.categories
    ph = PaginatorListHelper(
        elements=categories,
        prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
        items_per_page=ITEMS_PER_PAGE,
    )
    sm = SendMessage(message)
    page = int(message.data.split("#")[1])
    buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_CATEGORY, template=TEMPLATE_BUTTON_CATEGORY, page=page)
    sm.send_message(messages.for_paginator, inline_keyboard=ph.get_inline_keyboard(page_data=buttons))


@BOT.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == PREFIX_CATEGORY_ELEMENT_PAGINATOR,
    state=CategoriesStatesGroup.categories,
)
def handle_category_element(message: CallbackQuery):
    sm = SendMessage(message)
    category_index, page = (int(e) for e in message.data.split("#") if e.isdigit())
    with MainDataContextmanager(message) as md:
        categories = md.categories
    category = categories[category_index]
    text = templates.detail_md(category.name)
    inline_keyboard = KeyboardActionsByElement(page, category_index).get_inline_keyboard_category()
    sm.send_message(text, inline_keyboard=inline_keyboard, parse_mode="Markdown")
