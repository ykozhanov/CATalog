from src.frontend.telegram.handlers.commands import COMMANDS


class ProductUseActionMessages:
    @property
    def error_diff(self) -> str:
        return "Использованное количество должно быть положительным числом!\n"\
            "Попробуйте еще раз:"



class ProductUseActionTemplates:
    @staticmethod
    def old_md(name: str, unit: str, quantity: int) -> str:
        return "Вот сколько товара у вас еще осталось:\n\n"\
            f"\t\t\t*Имя*: {name}\n"\
            f"\t\t\t*Количество*: {quantity}\n"\
            f"\t\t\t*Единица измерения*: {unit}\n\n"\
            "Сколько товара вы использовали?"

    @staticmethod
    def error_diff(current_diff: float) -> str:
        return f"Использованное количество не может быть больше {current_diff}!\nПопробуйте еще раз:"

    @staticmethod
    def new_md(name: str, unit: str, quantity: int) -> str:
        return "Товар успешно обновлен!:\n\n"\
            f"\t\t\t*Имя*: {name}\n"\
            f"\t\t\t*Количество*: {quantity}\n"\
            f"\t\t\t*Единица измерения*: {unit}\n\n"\
            f"Вернуться к списку действий /{COMMANDS.help[0]}"

    @staticmethod
    def delete_md(name: str) -> str:
        return f"Товар *{name}* закончился и успешно удалён!\n\n"\
            f"Вернуться к списку действий /{COMMANDS.help[0]}"

