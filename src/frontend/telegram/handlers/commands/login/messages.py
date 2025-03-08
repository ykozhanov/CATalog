from src.frontend.telegram.handlers.commands import COMMANDS
from src.frontend.telegram.settings import APP_NAME


class LoginCommandMessages:
    @property
    def ask_register_again(self) -> str:
        return "Желаете зарегистрироваться снова?"

    @property
    def to_logout(self) -> str:
        return f"Для начала нужно выйти из аккаунта /{COMMANDS.logout[0]}."

    @property
    def input_username(self) -> str:
        return "Введите ваш никнейм:"

    @property
    def input_register_username(self) -> str:
        return "Придумайте никнейм:"

    @property
    def input_register_password(self) -> str:
        return "Придумайте пароль:"

    @property
    def input_register_password_repeat(self) -> str:
        return "Повторите пароль:"

    @property
    def invalid_register_password(self) -> str:
        return "Неверный пароль!\n\nПопробуйте снова придумать пароль:"

    @property
    def input_login_password(self) -> str:
        return "Введите пароль:"

    @property
    def input_email(self) -> str:
        return "Введите ваш email:"

    @property
    def invalid_email(self) -> str:
        return "Некорректный email, попробуйте снова:"


class LoginCommandTemplates:
    @staticmethod
    def check_md(username: str, email: str) -> str:
        return "Вы зарегистрируетесь со следующими учетными данными:\n\n"\
        f"\t\t\t*Никнейм*: {username}\n"\
        f"\t\t\t*Email*: {email}\n\n"\
        "Верно?"

    @staticmethod
    def got_exception(e: Exception) -> str:
        return "Что-то пошло не так!\n\n"\
            f"{str(e)}\n\n"\
            f"Используйте /{COMMANDS.login[0]} для повторного входа / регистрации."


    @staticmethod
    def after_login(username: str) -> str:
        return "Вы успешно зарегистрировались!\n"\
            f"Добро пожаловать {username}!\n\n"\
            f"Используйте /{COMMANDS.help[0]} для получения списка команд."

    @staticmethod
    def to_help(username: str) -> str:
        return f"Добро пожаловать {username}!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."

    @staticmethod
    def login_or_register(username: str) -> str:
        return f"Добро пожаловать {username}.\nВы уже зарегистрированы в приложении {APP_NAME}?"
