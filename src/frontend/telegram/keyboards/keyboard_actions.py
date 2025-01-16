from dataclasses import dataclass


@dataclass
class KeyboardListActions:
    item: int
    CALLBACK_EDIT: str = "edit"
    CALLBACK_DELETE: str = "delete"

    @property
    def answer_edit(self) -> str:
        return "Редактировать"

    @property
    def answer_delete(self) -> str:
        return "Удалить"

    @property
    def callback_answer_edit(self) -> str:
        return f"{self.CALLBACK_EDIT}#{self.item}"

    @property
    def callback_answer_delete(self) -> str:
        return f"{self.CALLBACK_DELETE}#{self.item}"

    def get_inline_keyboard(self) -> list[tuple[str, str]]:
        return [
            (self.answer_edit, self.callback_answer_edit),
            (self.answer_delete, self.callback_answer_delete),
        ]
