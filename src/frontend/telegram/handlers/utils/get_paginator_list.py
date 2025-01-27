from pydantic import BaseModel
from telebot.types import InlineKeyboardMarkup

from src.frontend.telegram.core.utils import PaginatorListHelper
from src.frontend.telegram.settings import ITEMS_PER_PAGE


def get_inline_paginator_list(
        elements: list[BaseModel],
        prefix_element: str,
        attrs_for_template: list[str],
        template: str,
        page: int = 1,
) -> InlineKeyboardMarkup:
    ph = PaginatorListHelper(
        elements=elements,
        prefix_element=prefix_element,
        items_per_page=ITEMS_PER_PAGE,
    )
    buttons = ph.get_buttons_for_page(attrs=attrs_for_template, template=template, page=page)
    return ph.get_inline_keyboard(page_data=buttons)
