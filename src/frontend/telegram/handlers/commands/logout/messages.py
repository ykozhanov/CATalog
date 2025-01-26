from src.frontend.telegram.handlers.commands import COMMANDS


class LogoutCommandMessages:
    @property
    def ask_logout(self) -> str:
        return "Вы действительно хотите выйти?"

    @property
    def callback_no(self) -> str:
        return f"Хорошо, используйте /{COMMANDS.help[0]} для получения списка доступных команд"

    @property
    def callback_yes(self) -> str:
        return f"Вы успешно вышли, используйте /{COMMANDS.login[0]} чтобы войти снова!"
