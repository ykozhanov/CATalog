from src.frontend.telegram.handlers.commands import COMMANDS


class GetProductsByNameActionMessages:
    @property
    def input_name(self) -> str:
        return "Введите название товара, которе хотите найти:"

class GetProductsByNameActionTemplates:
    @staticmethod
    def empty(name: str) -> str:
        return f"У вас пока нет ни одного товара с названием '{name}'.\n\n"\
            f"Вернуться к списку действий /{COMMANDS.help[0]}"


    @staticmethod
    def for_paginator(name: str) -> str:
        return f"Список товаров по названию '{name}':"

