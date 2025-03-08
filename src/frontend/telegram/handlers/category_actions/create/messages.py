MAX_LEN_NAME = 100


class CategoryCreateActionMessages:
    @property
    def input_name(self) -> str:
        return f"Введите название новой категории (не более {MAX_LEN_NAME} символов):"


    @property
    def try_again(self) -> str:
        return "Попробовать снова?"

    @property
    def success(self) -> str:
        return "Новая категория успешно создана!\nВернуться к списку действий /help"


class CategoryCreateActionTemplates:
    @staticmethod
    def check_md(
            name: str,
    ) -> str:
        return "Новая категория:\n\n"\
            f"\t\t\t*Имя*: {name}\n\n"\
            "Всё верно?"


    @staticmethod
    def error_max_len(max_len: int) -> str:
        return f"Длина превышает {max_len} символов!\nПопробуйте еще раз:"
