from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    PaginatorHelper,
)
from src.frontend.telegram.handlers.messages_helper import MESSAGES_ACTION_GET_ALL_CATEGORIES, MESSAGES_MAIN
from src.frontend.telegram.keyboards import KEYBOARD_LIST_ACTIONS, KEYBOARD_YES_OR_NO
from src.frontend.telegram.states import CategoriesStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.core.exceptions import CategoryError

PREFIX_CATEGORY_ELEMENT_PAGINATOR = "category"
ph = PaginatorHelper()


@check_authentication_decorator
@BOT.message_handler(
    func=lambda m: m == KEYBOARD_LIST_ACTIONS.action_get_all_categories,
    state=ActionsStatesGroup.choosing_action,
)
def handle_action_get_all_categories(message: Message) -> None:
    sm = SendMessage(message)
    sm.delete_reply_keyboard()
    try:
        with MainDataContextmanager as md:
            if a_token := md.user.access_jtw_token:
                p_api = CategoriesAPI(access_token=a_token)
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
            md.categories = p_api.get_all()
            categories = md.categories
    except CategoryError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
    if categories:
        category = categories[0]
        text = MESSAGES_ACTION_GET_ALL_CATEGORIES.template_message_get_list_all_categories_md(**category.model_dump())
        paginator = ph.get_list_paginator(page_count=len(categories), prefix_element=PREFIX_CATEGORY_ELEMENT_PAGINATOR)
        sm.send_message(
            text,
            parse_mode="Markdown",
            state=CategoriesStatesGroup.category,
            paginator_keyboard=paginator,
        )
    else:
        #TODO Добавить обработку в создание категории
        sm.send_message(
            text=MESSAGES_ACTION_GET_ALL_CATEGORIES.products_empty,
            state=CategoriesStatesGroup.ask_add_new_category,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
            delete_reply_keyboard=True,
        )

@BOT.callback_query_handler(
    func=lambda m: m.data == KEYBOARD_YES_OR_NO.callback_answer_no,
    state=CategoriesStatesGroup.ask_add_new_category,
)
def handle_state_ask_add_new_category_no(message: CallbackQuery) -> None:
    sm = SendMessage(message)
    sm.send_message(text=MESSAGES_MAIN.message_to_help, finish_state=True)
