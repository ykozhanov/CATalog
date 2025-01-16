from dataclasses import dataclass

from src.frontend.telegram.settings import APP_NAME
from src.frontend.telegram.handlers.commands import COMMANDS


@dataclass
class MessagesCommandLogin:
    app_name: str

    @property
    def message_ask_register_again(self) -> str:
        return "Желаете зарегистрироваться снова?"

    @property
    def message_to_logout(self) -> str:
        return f"Для начала нужно выйти из аккаунта /{COMMANDS.logout[0]}."

    @property
    def message_input_username(self) -> str:
        return "Введите ваш никнейм:"

    @property
    def message_input_register_username(self) -> str:
        return "Придумайте никнейм:"

    @property
    def message_input_register_password(self) -> str:
        return "Придумайте пароль:"

    @property
    def message_input_register_password_repeat(self) -> str:
        return "Повторите пароль:"

    @property
    def message_input_invalid_register_password_repeat(self) -> str:
        return "Неверный пароль!\n\nПопробуйте снова придумать пароль:"

    @property
    def message_input_login_password(self) -> str:
        return "Введите пароль:"

    @property
    def message_input_email(self) -> str:
        return "Введите ваш email:"

    @property
    def message_input_invalid_email(self) -> str:
        return "Некорректный email, попробуйте снова:"

    @staticmethod
    def template_message_check_register_md(username: str, email: str) -> str:
        return f"""Вы зарегистрируетесь со следующими учетными данными:
        **Никнейм**: {username};
        **Email**: {email}.
        
        Верно?
        """

    @staticmethod
    def template_message_got_exception(e: Exception) -> str:
        return f"""Что-то пошло не так!

        {str(e)}

        Используйте /{COMMANDS.login[0]} для повторного входа / регистрации.
        """

    @staticmethod
    def template_message_after_login(username: str) -> str:
        return f"""Вы успешно зарегистрировались!
        Добро пожаловать {username}.
        
        Используйте /{COMMANDS.help[0]} для получения списка команд.
        """

    @staticmethod
    def template_message_to_help(username: str) -> str:
        return f"Добро пожаловать {username}!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."


MESSAGES_COMMAND_LOGIN = MessagesCommandLogin(app_name=APP_NAME)
