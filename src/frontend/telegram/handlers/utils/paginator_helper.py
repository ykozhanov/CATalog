from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton

class PaginatorHelper:
    CALLBACK_EDIT = "edit"
    CALLBACK_DELETE = "delete"
    CALLBACK_CREATE = "create"

    def get_list_paginator(self, page_count: int, prefix_element: str, page: int = 1) -> InlineKeyboardPaginator:
        paginator = InlineKeyboardPaginator(
                page_count=page_count,
                current_page=page,
                data_pattern=f"{prefix_element}#{{page}}",
            )
        paginator.add_before(
            InlineKeyboardButton(text="Редактировать", callback_data=f"{self.CALLBACK_EDIT}#{page}"),
            InlineKeyboardButton(text="Удалить", callback_data=f"{self.CALLBACK_DELETE}#{page}"),
        )
        paginator.add_after(
            InlineKeyboardButton(text="Создать", callback_data=f"{self.CALLBACK_CREATE}#{page}"),
        )
        return paginator
