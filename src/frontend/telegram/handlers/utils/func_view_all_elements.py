from typing import TypeVar

from telebot import State
from telebot.types import Message, CallbackQuery
from pydantic import BaseModel

from src.frontend.telegram.settings import ITEMS_PER_PAGE
from src.frontend.telegram.core.utils import SendMessage, PaginatorHelper
from src.frontend.telegram.keyboards import KEYBOARD_YES_OR_NO


T = TypeVar("T", bound=BaseModel)

def handle_action_get_all_elements(
        message: Message | CallbackQuery,
        prefix_element_paginator: str,
        attrs_for_template: list[str],
        template_button: str,
        elements: list[T],
        text_for_paginator: str,
        text_for_paginator_empty: str,
        state_paginator: State,
        state_add_new_element: State | None = None,
) -> None:
    sm = SendMessage(message)
    if elements:
        ph = PaginatorHelper(
            elements=elements,
            prefix_element=prefix_element_paginator,
            items_per_page=ITEMS_PER_PAGE,
        )
        buttons = ph.get_buttons_for_page(attrs=attrs_for_template, template=template_button)
        sm.send_message(
            text=text_for_paginator,
            state=state_paginator,
            inline_keyboard=ph.get_inline_keyboard(page_data=buttons),
        )
    else:
        #TODO Добавить обработку в создание
        sm.send_message(
            text=text_for_paginator_empty,
            state=state_add_new_element,
            inline_keyboard=KEYBOARD_YES_OR_NO.get_inline_keyboard(),
            delete_reply_keyboard=True,
            finish_state=True if state_add_new_element is None else False,
        )
