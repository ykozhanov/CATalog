from dataclasses import dataclass

from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.settings import EXP_DAYS


@dataclass
class MessagesActionGetProductsByExpDate:

    @property
    def message_input_name_product(self) -> str:
        return "Введите название товара, которе хотите найти:"

    @property
    def message_products_empty(self) -> str:
        return f"""У вас пока нет ни одного товара с истекающим сроком годности.
        
        Вернуться к списку действий /{COMMANDS.help[0]}
        """

    @property
    def message_for_paginator(self) -> str:
        return f"Список товаров, срок годности которых истекает через {EXP_DAYS} дня (дней):"


MESSAGES_ACTION_GET_PRODUCTS_BY_EXP_DATE = MessagesActionGetProductsByExpDate()
