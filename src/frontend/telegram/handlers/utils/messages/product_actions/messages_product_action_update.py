from datetime import date
from dataclasses import dataclass

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE


@dataclass
class MessagesActionProductUpdate:

    @property
    def message_ask_input_name(self) -> str:
        return "Хотите изменить название товара?"

    @property
    def message_input_name(self) -> str:
        return "Введите название товара:"

    @property
    def message_ask_input_unit(self) -> str:
        return "Хотите изменить единицу измерения?"

    @property
    def message_input_unit(self) -> str:
        return "Введите единицу измерения:"

    @property
    def message_ask_input_quantity(self) -> str:
        return "Хотите изменить количество?"

    @property
    def message_input_quantity(self) -> str:
        return "Введите количество:"

    @property
    def message_error_quantity(self) -> str:
        return "Количество должно быть числом!\nПопробуйте еще раз:"

    @property
    def message_ask_input_exp_date(self) -> str:
        return "Хотите изменить срок годности?"

    @property
    def message_input_day(self) -> str:
        return "Введите день:"

    @property
    def message_error_day(self) -> str:
        return "День должен быть числом от 1 до 31!\nПопробуйте еще раз:"

    @property
    def message_input_month(self) -> str:
        return "Введите месяц:"

    @property
    def message_error_month(self) -> str:
        return "Месяц должен быть числом от 1 до 12!\nПопробуйте еще раз:"

    @property
    def message_input_year(self) -> str:
        return "Введите год:"

    @property
    def message_error_year(self) -> str:
        return "Некорректный формат года!\nПопробуйте еще раз:"

    @property
    def message_ask_input_note(self) -> str:
        return "Хотите изменить примечание?"

    @property
    def message_input_note(self) -> str:
        return "Введите примечание:"

    @property
    def message_ask_choice_category(self) -> str:
        return "Хотите изменить категорию?"

    @property
    def message_choice_category(self) -> str:
        return "Выберите категорию:"

    @property
    def message_try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def message_success_update(self) -> str:
        return "Товар успешно обновлен!\nВернуться к списку действий /help"

    @staticmethod
    def template_message_check(
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


MESSAGES_ACTION_PRODUCT_UPDATE = MessagesActionProductUpdate()
