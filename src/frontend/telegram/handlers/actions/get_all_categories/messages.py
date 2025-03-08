class GetAllCategoriesActionMessages:
    @property
    def empty(self) -> str:
        return "У вас пока нет ни одной категории, добавить?"

    @property
    def for_paginator(self) -> str:
        return "Список категорий:"


class GetAllCategoriesActionTemplates:
    @staticmethod
    def detail_md(name: str) -> str:
        return "О категории:\n\n"\
            f"\t\t\t*Имя**: {name}"
