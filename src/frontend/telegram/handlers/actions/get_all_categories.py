from telebot.types import Message, CallbackQuery

from src.frontend.telegram.settings import BOT
from src.frontend.telegram.core.utils import SendMessage
from src.frontend.telegram.handlers.utils import (
    MainDataContextmanager,
    check_authentication_decorator,
    handle_action_get_all_elements,
)
from src.frontend.telegram.handlers.messages_helper import MESSAGES_ACTION_GET_ALL_CATEGORIES, MESSAGES_MAIN
from src.frontend.telegram.keyboards import KEYBOARD_LIST_ACTIONS, KEYBOARD_YES_OR_NO
from src.frontend.telegram.states import CategoriesStatesGroup, ActionsStatesGroup
from src.frontend.telegram.api import CategoriesAPI
from src.frontend.telegram.core.exceptions import CategoryError
from . import PREFIX_CATEGORY_ELEMENT_PAGINATOR, ATTRS_FOR_TEMPLATE_CATEGORY, TEMPLATE_BUTTON_CATEGORY


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
                c_api = CategoriesAPI(access_token=a_token)
            else:
                sm.send_message(text=MESSAGES_MAIN.message_something_went_wrong, finish_state=True)
                return
            categories = md.categories = c_api.get_all()
    except CategoryError as e:
        sm.send_message(text=MESSAGES_MAIN.template_message_got_exception(e), finish_state=True)
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
