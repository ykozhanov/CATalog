import datetime
import math
from typing import TypeVar, Any, Callable

from pydantic import BaseModel
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE, VIEW_NONE

T = TypeVar("T", bound=BaseModel)


class FormatterTemplateDataAttrs:
    __formatters_data_for_templates = {
        datetime.date: "formater_date",
        type(None): "formater_none",
    }

    def __init__(self, data: Any):
        self.data = data
        self.formatter = self.get_formatter(self.data)

    def get_formatter(self, data: Any) -> Callable[..., str]:
        data_type = type(data)
        call = self.__formatters_data_for_templates.get(data_type, None)
        if not call:
            return self.default_formatter
        return getattr(self, call)

    @classmethod
    def formater_date(cls, data: datetime.date) -> str:
        return data.strftime(DISPLAY_DATE_FORMATE)

    @classmethod
    def formater_none(cls, data: None) -> str:
        return VIEW_NONE

    @classmethod
    def default_formatter(cls, data: Any) -> str:
        return str(data)

    def formatted_data(self) -> str:
        return self.formatter(self.data)



class PaginatorListHelper:
    CALLBACK_CREATE = "create"
    CALLBACK_PAGE = "page"

    def __init__(self, elements: list[T], prefix_element: str, items_per_page: int = 5, add_create: bool = True):
        self.prefix_element = prefix_element
        self._elements = elements
        self._items_per_page = items_per_page
        self._page_count = math.ceil(len(elements) / items_per_page)
        self._add_create = add_create


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


    @staticmethod
    def _get_data_for_template(elem: T, attrs: list[str]) -> dict[str, Any]:
        data_for_template = {}
        for attr in attrs:
            attr_data = getattr(elem, attr)
            formatted_attr_data = FormatterTemplateDataAttrs(attr_data).formatted_data()
            data_for_template[attr] = formatted_attr_data
        return data_for_template

    def get_buttons_for_page(self, attrs: list[str], template: str, page: int = 1) -> list[InlineKeyboardButton]:
        get_elements = self._get_list_elements_for_page(page)
        buttons = []
        for elem in get_elements:
            for_template = self._get_data_for_template(elem, attrs)
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
        if self._add_create:
            keyboard.row(InlineKeyboardButton(text="Создать 🆕", callback_data=self.CALLBACK_CREATE))
        return keyboard
