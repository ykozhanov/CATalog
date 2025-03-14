from src.frontend.telegram.settings import APP_NAME
from src.frontend.telegram.handlers.commands import COMMANDS


class MainMessages:
    @property
    def to_help(self) -> str:
        return f"Для выбора действия воспользуйтесь /{COMMANDS.help[0]}"

    @property
    def to_login(self) -> str:
        return f"Войдите пожалуйста в приложение {APP_NAME} /{COMMANDS.login[0]}."

    @property
    def something_went_wrong(self) -> str:
        return f"Что-то пошло не так!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."

    @staticmethod
    def t_got_exception(e: Exception) -> str:
        return "Что-то пошло не так!\n\n"\
            f"{str(e)}\n\n"\
            f"Используйте /{COMMANDS.help[0]} для получения списка команд."
