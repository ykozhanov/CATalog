from datetime import date
from dataclasses import dataclass

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE


@dataclass
class MessagesActionGetAllProducts:

    @property
    def message_products_empty(self) -> str:
        return "У вас пока нет ни одного товара, добавить?"

    @property
    def message_for_paginator(self) -> str:
        return "Список товаров:"

    # @staticmethod
    # def template_message_get_list_detail_product_md(
    #         name: str,
    #         unit: str,
    #         quantity: int,
    #         exp_date: date,
    #         note: str,
    # ) -> str:
    #     return f"""О товаре:
    #         **Имя**: {name};
    #         **Количество**: {quantity};
    #         **Единица измерения**: {unit};
    #         **Срок годности (до)**: {exp_date.strftime(DISPLAY_DATE_FORMATE) if exp_date else "без срока годности"};
    #         **Заметки**: {note if note else ""}
    #     """


MESSAGES_ACTION_GET_ALL_PRODUCTS = MessagesActionGetAllProducts()
