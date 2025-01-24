from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT, ITEMS_PER_PAGE
from src.frontend.telegram.core.utils import SendMessage, PaginatorHelper
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    handle_action_get_all_elements,
)
from src.frontend.telegram.handlers.utils.messages import MESSAGES_ACTION_GET_ALL_CATEGORIES, MESSAGES_MAIN
from src.frontend.telegram.bot.keyboards import KEYBOARD_LIST_ACTIONS, KEYBOARD_YES_OR_NO, KeyboardActionsByElement
from src.frontend.telegram.bot.states import CategoriesStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.api.categories.schemas import CategoryInSchema
from src.frontend.telegram.core.exceptions import CategoryError
from . import PREFIX_CATEGORY_ELEMENT_PAGINATOR, ATTRS_FOR_TEMPLATE_CATEGORY, TEMPLATE_BUTTON_CATEGORY


def get_all_categories(message: Message | CallbackQuery) -> list[CategoryInSchema] | None:
    with MainDataContextmanager(message) as md:
        if a_token := md.user.access_jtw_token:
            c_api = CategoriesAPI(a_token)
            md.categories = c_api.get_all()
            return md.categories
        else:
            return None


@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m.text == KEYBOARD_LIST_ACTIONS.action_get_all_categories,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_categories(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    try:
        if categories := get_all_categories(message) is None:
            sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
            return
    except CategoryError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    else:
        handle_action_get_all_elements(
            message=message,
            prefix_element_paginator=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
            attrs_for_template=ATTRS_FOR_TEMPLATE_CATEGORY,
            template_button=TEMPLATE_BUTTON_CATEGORY,
            elements=categories,
            text_for_paginator=MESSAGES_ACTION_GET_ALL_CATEGORIES.message_for_paginator,
            text_for_paginator_empty=MESSAGES_ACTION_GET_ALL_CATEGORIES.message_categories_empty,
            state_paginator=CategoriesStatesGroup.categories,
            state_add_new_element=CategoriesStatesGroup.ask_add_new_category,
        )

@BOT.callback_query_handler(
    func=lambda m: m.data == KEYBOARD_YES_OR_NO.callback_answer_no,
    state=CategoriesStatesGroup.ask_add_new_category,
)
def handle_state_ask_add_new_category_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=MESSAGES_MAIN.message_to_help, finish_state=True)


@check_authentication_decorator
@BOT.callback_query_handler(
    func=lambda m: m.split("#")[0] == PaginatorHelper.CALLBACK_PAGE,
    state=CategoriesStatesGroup.categories,
)
def handle_categories_paginator(message: CallbackQuery):
    with MainDataContextmanager(message) as md:
        categories = md.categories
    ph = PaginatorHelper(
        elements=categories,
        prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR,
        items_per_page=ITEMS_PER_PAGE,
    )
    sm = SendMessage(message)
    page = int(message.data.split("#")[1])
    buttons = ph.get_buttons_for_page(attrs=ATTRS_FOR_TEMPLATE_CATEGORY, template=TEMPLATE_BUTTON_CATEGORY, page=page)
    sm.send_message(
        text=MESSAGES_ACTION_GET_ALL_CATEGORIES.message_for_paginator,
        inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
    )


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
    text = MESSAGES_ACTION_GET_ALL_CATEGORIES.template_message_get_list_all_categories_md(name=category.name)
    inline_keyboard = KeyboardActionsByElement(page).get_inline_keyboard_category()
    sm.send_message(text, inline_keyboard=inline_keyboard)
