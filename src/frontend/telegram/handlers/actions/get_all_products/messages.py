from datetime import date

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE


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
        return f"""О товаре:
            **Имя**: {name};
            **Количество**: {quantity};
            **Единица измерения**: {unit};
            **Срок годности (до)**: {exp_date.strftime(DISPLAY_DATE_FORMATE) if exp_date else "без срока годности"};
            **Примечание**: {note if note else ""};
            **Категория**: {category}.
        """
