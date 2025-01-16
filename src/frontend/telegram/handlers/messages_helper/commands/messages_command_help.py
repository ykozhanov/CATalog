from dataclasses import dataclass

from src.frontend.telegram.handlers.commands import COMMANDS


@dataclass
class MessagesCommandHelp:

    @property
    def message_list_actions(self) -> str:
        return "Вот список команд, что хотите сделать?"

    @property
    def message_to_login(self) -> str:
        return f"Для начала вам нужно войти /{COMMANDS.login[0]}"


MESSAGES_COMMAND_HELP = MessagesCommandHelp()
