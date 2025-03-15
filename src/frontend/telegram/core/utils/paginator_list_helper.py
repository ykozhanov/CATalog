import math
from typing import TypeVar

from pydantic import BaseModel
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

T = TypeVar("T", bound=BaseModel)


class PaginatorListHelper:
    CALLBACK_CREATE = "create"
    CALLBACK_PAGE = "page"

    def __init__(self, elements: list[T], prefix_element: str, items_per_page: int = 5):
        self.prefix_element = prefix_element
        self._elements = elements
        self._items_per_page = items_per_page
        self._page_count = math.ceil(len(elements) / items_per_page)

    def _get_paginator_keys(self, page: int) -> list[InlineKeyboardButton]:
        paginator_keys = []
        start = 1
        end = self._page_count

        if page > 1:
            # Добавляем кнопку "В начало"
            paginator_keys.append(InlineKeyboardButton(str(start), callback_data=f"{self.CALLBACK_PAGE}#{start}"))
            # Добавляем кнопку "Предыдущая"
            paginator_keys.append(InlineKeyboardButton(str(page - 1), callback_data=f"{self.CALLBACK_PAGE}#{page - 1}"))
            # Добавляем текущую страницу
            paginator_keys.append(InlineKeyboardButton(str(page), callback_data=f"{self.CALLBACK_PAGE}#{page}"))

        # Добавляем кнопку "Следующая"
        if page < end:
            paginator_keys.append(InlineKeyboardButton(str(page + 1), callback_data=f"{self.CALLBACK_PAGE}#{page + 1}"))

        # Добавляем кнопку "В конец"
        if page < end:
            paginator_keys.append(InlineKeyboardButton(str(end), callback_data=f"{self.CALLBACK_PAGE}#{end}"))

        return paginator_keys

    def _get_list_elements_for_page(self, page: int) -> list[T]:
        start = (page - 1) * self._items_per_page
        end = start + self._items_per_page
        if end > len(self._elements):
            end = len(self._elements)
        return self._elements[start:end]

    def get_buttons_for_page(self, attrs: list[str], template: str, page: int = 1) -> list[InlineKeyboardButton]:
        get_elements = self._get_list_elements_for_page(page)
        buttons = []
        for elem in get_elements:
            for_template = {attr: getattr(elem, attr) for attr in attrs}
            text = template.format(**for_template)
            index = self._elements.index(elem)
            buttons.append(InlineKeyboardButton(text=text, callback_data=f"{self.prefix_element}#{index}#{page}"))
        del for_template
        return buttons

    def get_inline_keyboard(self, page_data: list[InlineKeyboardButton], page: int = 1) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for b in page_data:
            keyboard.row(b)
        keyboard.row(*self._get_paginator_keys(page))
        keyboard.row(InlineKeyboardButton(text=">> Создать <<", callback_data=self.CALLBACK_CREATE))
        return keyboard
