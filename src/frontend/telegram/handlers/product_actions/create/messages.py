from datetime import date

from src.frontend.telegram.settings import DISPLAY_DATE_FORMATE, VIEW_NONE

MAX_LEN_NAME = 100
MAX_LEN_UNIT = 10
MAX_LEN_NOTE = 500


class ProductCreateActionMessages:
    @property
    def input_name(self) -> str:
        return f"Введите название нового товара (не более {MAX_LEN_NAME} символов):"

    @property
    def input_unit(self) -> str:
        return f"Введите единицу измерения (не более {MAX_LEN_UNIT} символов):"

    @property
    def input_quantity(self) -> str:
        return "Введите количество:"

    @property
    def error_quantity(self) -> str:
        return "Количество должно быть положительным числом!\nПопробуйте еще раз:"

    @property
    def ask_input_exp_date(self) -> str:
        return "Хотите установить срок годности?"

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
        return "Хотите добавить примечание?"

    @property
    def input_note(self) -> str:
        return f"Введите примечание (не более {MAX_LEN_NOTE} символов):"

    @property
    def choice_category(self) -> str:
        return "Выберите категорию:"

    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Новый товар успешно создан!\nВернуться к списку действий /help"


class ProductCreateActionTemplates:
    @staticmethod
    def check_md(
            name: str,
            unit: str,
            quantity: int,
            exp_date: date,
            note: str,
            category: str,
    ) -> str:
        return "Новый товар:\n\n"\
            f"\t\t\t*Имя*: {name}\n"\
            f"\t\t\t*Количество*: {quantity}\n"\
            f"\t\t\t*Единица измерения*: {unit}\n"\
            f"\t\t\t*Срок годности (до)*: {exp_date.strftime(DISPLAY_DATE_FORMATE) if exp_date else VIEW_NONE}\n"\
            f"\t\t\t*Примечание*: {note if note else VIEW_NONE}\n"\
            f"\t\t\t*Категория*: {category}\n\n"\
            "Всё верно?"

    @staticmethod
    def error_max_len(max_len: int) -> str:
        return f"Длина превышает {max_len} символов!\nПопробуйте еще раз:"
