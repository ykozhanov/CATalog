from datetime import date

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE


class ProductUpdateActionMessages:
    @property
    def ask_input_name(self) -> str:
        return "Хотите изменить название товара?"

    @property
    def input_name(self) -> str:
        return "Введите название товара:"

    @property
    def ask_input_unit(self) -> str:
        return "Хотите изменить единицу измерения?"

    @property
    def input_unit(self) -> str:
        return "Введите единицу измерения:"

    @property
    def ask_input_quantity(self) -> str:
        return "Хотите изменить количество?"

    @property
    def input_quantity(self) -> str:
        return "Введите количество:"

    @property
    def error_quantity(self) -> str:
        return "Количество должно быть числом!\nПопробуйте еще раз:"

    @property
    def ask_input_exp_date(self) -> str:
        return "Хотите изменить срок годности?"

    @property
    def input_day(self) -> str:
        return "Введите день:"

    @property
    def error_day(self) -> str:
        return "День должен быть числом от 1 до 31!\nПопробуйте еще раз:"

    @property
    def input_month(self) -> str:
        return "Введите месяц:"

    @property
    def error_month(self) -> str:
        return "Месяц должен быть числом от 1 до 12!\nПопробуйте еще раз:"

    @property
    def input_year(self) -> str:
        return "Введите год:"

    @property
    def error_year(self) -> str:
        return "Некорректный формат года!\nПопробуйте еще раз:"

    @property
    def ask_input_note(self) -> str:
        return "Хотите изменить примечание?"

    @property
    def input_note(self) -> str:
        return "Введите примечание:"

    @property
    def ask_choice_category(self) -> str:
        return "Хотите изменить категорию?"

    @property
    def choice_category(self) -> str:
        return "Выберите категорию:"

    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Товар успешно обновлен!\nВернуться к списку действий /help"


class ProductUpdateActionTemplates:
    @staticmethod
    def check_md(
            name: str,
            unit: str,
            quantity: int,
            exp_date: date,
            note: str,
            category: str,
    ) -> str:
        return f"""Обновленный товар:
            **Имя**: {name};
            **Количество**: {quantity};
            **Единица измерения**: {unit};
            **Срок годности (до)**: {exp_date.strftime(DISPLAY_DATE_FORMATE) if exp_date else "без срока годности"};
            **Примечание**: {note if note else ""};
            **Категория**: {category}.
        
        Всё верно?
        """
