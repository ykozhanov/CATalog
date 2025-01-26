from telebot.types import BotCommand

from src.frontend.telegram.settings import APP_NAME, BOT


class Commands:

    @property
    def start(self) -> tuple[str, str]:
        return "start", "Запустить бот"

    @property
    def login(self) -> tuple[str, str]:
        return "login", f"Войти в аккаунт {APP_NAME} или зарегистрироваться"

    @property
    def help(self) -> tuple[str, str]:
        return "help", "Показать список команд"

    @property
    def logout(self) -> tuple[str, str]:
        return "logout", f"Выйти из аккаунта {APP_NAME}"


COMMANDS = Commands()

BOT.set_my_commands(
    [
        BotCommand(command=f"/{COMMANDS.start[0]}", description=COMMANDS.start[1]),
        BotCommand(command=f"/{COMMANDS.login[0]}", description=COMMANDS.login[1]),
        BotCommand(command=f"/{COMMANDS.logout[0]}", description=COMMANDS.logout[1]),
        BotCommand(command=f"/{COMMANDS.help[0]}", description=COMMANDS.help[1]),
    ]
)

__all__ = ["COMMANDS"]