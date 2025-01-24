from dataclasses import dataclass

from src.frontend.telegram.settings import APP_NAME

from src.frontend.telegram.handlers.commands import COMMANDS


@dataclass
class MessagesMain:
    app_name: str

    @property
    def message_to_help(self) -> str:
        return f"Для выбора действия воспользуйтесь {COMMANDS.help[0]}"

    @property
    def message_start(self) -> str:
        return f"Добро пожаловать!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."

    @property
    def message_to_login(self) -> str:
        return f"Войдите пожалуйста в приложение {self.app_name} /{COMMANDS.login[0]}."

    @property
    def message_something_went_wrong(self) -> str:
        return f"Что-то пошло не так!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."

    @staticmethod
    def template_message_got_exception(e: Exception) -> str:
        return f"""
        Что-то пошло не так!
        
        {str(e)}
        
        Используйте /{COMMANDS.help[0]} для получения списка команд.
        """


MESSAGES_MAIN = MessagesMain(app_name=APP_NAME)
