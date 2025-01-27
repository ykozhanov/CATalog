from src.frontend.telegram.handlers.commands import COMMANDS


class ProductUseActionMessages:
    @property
    def error_diff(self) -> str:
        return "Использованное количество должно быть положительным числом!\nПопробуйте еще раз:"



class ProductUseActionTemplates:
    @staticmethod
    def old_md(name: str, unit: str, quantity: int) -> str:
        return f"""Вот сколько товара у вас еще осталось:
            **Имя**: {name};
            **Количество**: {quantity};
            **Единица измерения**: {unit}.

        Сколько товара вы использовали?
        """

    @staticmethod
    def error_diff(current_diff: float) -> str:
        return f"Использованное количество не может быть больше {current_diff}!\nПопробуйте еще раз:"

    @staticmethod
    def new_md(name: str, unit: str, quantity: int) -> str:
        return f"""Товар успешно обновлен!:
                    **Имя**: {name};
                    **Количество**: {quantity};
                    **Единица измерения**: {unit}.

                Вернуться к списку действий /{COMMANDS.help[0]}
                """

    @staticmethod
    def delete_md(name: str) -> str:
        return f"""Товар **{name}** закончился и успешно удалён!
        
                Вернуться к списку действий /{COMMANDS.help[0]}
                """
