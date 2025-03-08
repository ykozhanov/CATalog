from src.frontend.telegram.handlers.category_actions.create.messages import MAX_LEN_NAME


class CategoryUpdateActionMessages:
    @property
    def input_name(self) -> str:
        return f"Введите новое название товара (не более {MAX_LEN_NAME} символов):"

    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Категория успешно обновлена!\nВернуться к списку действий /help"


class CategoryUpdateActionTemplates:
    @staticmethod
    def check_md(name: str) -> str:
        return f"Обновленная категория:\n\n"\
            f"\t\t\t*Имя*: {name}\n\n"\
            "Всё верно?"

    @staticmethod
    def error_max_len(max_len: int) -> str:
        return f"Длина превышает {max_len} символов!\nПопробуйте еще раз:"

