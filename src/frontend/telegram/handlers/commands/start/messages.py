from src.frontend.telegram.handlers.commands import COMMANDS


class StartCommandMessages:
    @property
    def start(self) -> str:
        return f"Добро пожаловать!\n\nИспользуйте /{COMMANDS.help[0]} для получения списка команд."
