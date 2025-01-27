from datetime import date

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE


class CategoryUpdateActionMessages:
    @property
    def input_name(self) -> str:
        return "Введите новое название товара:"

    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Категория успешно обновлена!\nВернуться к списку действий /help"


class CategoryUpdateActionTemplates:
    @staticmethod
    def check_md(name: str) -> str:
        return f"""Обновленная категория:
            **Имя**: {name}.
        
        Всё верно?
        """
