import logging
from telebot.types import Message, CallbackQuery

from src.frontend.telegram.bot import telegram_bot
from src.frontend.telegram.core.utils import SendMessage, PaginatorListHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    MainMessages,
    exc_handler_decorator,
    check_authentication_decorator,
    get_inline_paginator_list, escape_markdown,
)
from src.frontend.telegram.bot.keyboards import KeyboardYesOrNo, KeyboardActionsByElement, k_list_actions
from src.frontend.telegram.bot.states import ActionsStatesGroup, CategoriesStatesGroup
from src.frontend.telegram.handlers.category_actions.create.states import CategoryCreateStatesGroup

from .messages import GetAllCategoriesActionMessages, GetAllCategoriesActionTemplates
from .utils import (
    get_all_categories,
    PREFIX_CATEGORY_ELEMENT_PAGINATOR,
    ATTRS_FOR_TEMPLATE_CATEGORY,
    TEMPLATE_BUTTON_CATEGORY,
)

__all__ = ["handle_action_get_all_categories"]


main_m = MainMessages()
messages = GetAllCategoriesActionMessages()
templates = GetAllCategoriesActionTemplates()
y_or_n = KeyboardYesOrNo()
paginator_callbacks = (PaginatorListHelper.CALLBACK_PAGE, KeyboardActionsByElement.BACK_PREFIX)


@telegram_bot.message_handler(func=lambda m: m.text == k_list_actions.action_get_all_categories)
@exc_handler_decorator
@check_authentication_decorator
def handle_action_get_all_categories(message: Message) -> None:
    logging.info("Старт 'handle_action_get_all_categories'")
    sm = SendMessage(message)
    categories = get_all_categories(message)
    logging.debug(f"{categories=}")

    if categories is None:
        logging.info("Конец 'handle_action_get_all_categories'")
        return sm.send_message(main_m.something_went_wrong, finish_state=True)

    if categories:
        inline_keyboard = get_inline_paginator_list(
            elements=categories,
            prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_CATEGORY,
            template=TEMPLATE_BUTTON_CATEGORY,
        )
        sm.send_message(
            messages.for_paginator,
            state=CategoriesStatesGroup.categories,
            inline_keyboard=inline_keyboard,
        )
    else:
        sm.send_message(
            text=messages.empty,
            state=CategoryCreateStatesGroup.ask_add_new,
            inline_keyboard=y_or_n.get_inline_keyboard(),
        )
    logging.info("Конец 'handle_action_get_all_categories'")


@telegram_bot.callback_query_handler(
    func=lambda m: m.data == y_or_n.callback_answer_no,
    state=CategoryCreateStatesGroup.ask_add_new,
)
def handle_state_ask_add_new_category_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(main_m.to_help, finish_state=True)


@telegram_bot.callback_query_handler(
    func=lambda m: m.data.split("#")[0] in paginator_callbacks,
    state=CategoriesStatesGroup.categories,
)
@check_authentication_decorator
def handle_categories_paginator(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        categories = md.categories
    sm = SendMessage(message)
    sm.delete_message()
    inline_keyboard = get_inline_paginator_list(
        elements=categories,
        prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
        attrs_for_template=ATTRS_FOR_TEMPLATE_CATEGORY,
        template=TEMPLATE_BUTTON_CATEGORY,
        page=int(message.data.split("#")[1]),
    )
    sm.send_message(messages.for_paginator, inline_keyboard=inline_keyboard)


@telegram_bot.callback_query_handler(
    func=lambda m: m.data.split("#")[0] == PREFIX_CATEGORY_ELEMENT_PAGINATOR,
    state=CategoriesStatesGroup.categories,
)
@exc_handler_decorator
def handle_category_element(message: CallbackQuery):
    sm = SendMessage(message)
    sm.delete_message()
    category_index, page = (int(e) for e in message.data.split("#") if e.isdigit())
    with MainDataContextmanager(message) as md:
        categories = md.categories
    category = categories[category_index]
    text = templates.detail_md(escape_markdown(category.name))
    inline_keyboard = KeyboardActionsByElement(page, category_index).get_inline_keyboard_category()
    sm.send_message(text, inline_keyboard=inline_keyboard, parse_mode="Markdown")
