from dataclasses import dataclass

from src.frontend.telegram.handlers.commands import COMMANDS


@dataclass
class MessagesActionGetProductsByName:

    @property
    def message_input_name_product(self) -> str:
        return "Введите название товара, которе хотите найти:"

    @staticmethod
    def template_message_products_empty(name: str) -> str:
        return f"""У вас пока нет ни одного товара с названием '{name}'.
        
        Вернуться к списку действий /{COMMANDS.help[0]}
        """

    @staticmethod
    def template_message_for_paginator(name: str) -> str:
        return f"Список товаров по названию '{name}':"


MESSAGES_ACTION_GET_PRODUCTS_BY_NAME = MessagesActionGetProductsByName()
