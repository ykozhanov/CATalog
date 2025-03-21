from datetime import date

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE, VIEW_NONE


class GetAllProductsActionMessages:
    @property
    def empty(self) -> str:
        return "У вас пока нет ни одного товара, добавить?"

    @property
    def for_paginator(self) -> str:
        return "Список товаров:"


class GetAllProductsActionTemplates:
    @staticmethod
    def detail_md(
            name: str,
            unit: str,
            quantity: int,
            exp_date: date,
            note: str,
            category: str,
    ) -> str:
        return "О товаре:\n\n"\
            f"\t\t\t*Имя*: {name}\n"\
            f"\t\t\t*Количество*: {quantity}\n"\
            f"\t\t\t*Единица измерения*: {unit}\n"\
            f"\t\t\t*Срок годности (до)*: {exp_date.strftime(DISPLAY_DATE_FORMATE) if exp_date else VIEW_NONE}\n"\
            f"\t\t\t*Примечание*: {note if note else VIEW_NONE}\n"\
            f"\t\t\t*Категория*: {category if category else VIEW_NONE}"
