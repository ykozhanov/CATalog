from dataclasses import dataclass

from src.frontend.telegram.handlers.commands import COMMANDS


@dataclass
class MessagesCommandLogout:

    @property
    def message_ask_logout(self) -> str:
        return "Вы действительно хотите выйти?"

    @property
    def message_to_login(self) -> str:
        return f"Для начала вам нужно войти /{COMMANDS.login[0]}"

    @property
    def message_callback_no(self) -> str:
        return f"Хорошо, используйте /{COMMANDS.help[0]} для получения списка доступных команд"

    @property
    def message_callback_yes(self) -> str:
        return f"Вы успешно вышли, используйте /{COMMANDS.login[0]} чтобы войти снова!"

MESSAGES_COMMAND_LOGOUT = MessagesCommandLogout()
