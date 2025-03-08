from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.settings import EXP_DAYS


class GetProductsByExpDateActionMessages:

    @property
    def input_name(self) -> str:
        return "Введите название товара, которе хотите найти:"

    @property
    def empty(self) -> str:
        return "У вас пока нет ни одного товара с истекающим сроком годности.\n\n"\
            f"Вернуться к списку действий /{COMMANDS.help[0]}"


    @property
    def for_paginator(self) -> str:
        return f"Список товаров, срок годности которых истекает через {EXP_DAYS} дня (дней):"
