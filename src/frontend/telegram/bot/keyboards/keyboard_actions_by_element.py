from dataclasses import dataclass


@dataclass
class KeyboardActionsByElement:
    page: int

    @property
    def answer_update(self) -> str:
        return "Обновить"

    @property
    def answer_delete(self) -> str:
        return "Удалить"

    @property
    def answer_use(self) -> str:
        return "Использовать"

    @property
    def answer_back(self) -> str:
        return "Использовать"

    @property
    def callback_answer_update(self) -> str:
        return "update"

    @property
    def callback_answer_delete(self) -> str:
        return "delete"

    @property
    def callback_answer_use(self) -> str:
        return "use"

    def callback_answer_back(self) -> str:
        return f"back#{self.page}"

    def get_inline_keyboard_product(self) -> list[tuple[str, str]]:
        return [
            (self.answer_update, self.callback_answer_update),
            (self.answer_delete, self.callback_answer_delete),
            (self.answer_use, self.callback_answer_use),
            (self.answer_back, self.callback_answer_back),
        ]

    def get_inline_keyboard_category(self) -> list[tuple[str, str]]:
        return [
            (self.answer_update, self.callback_answer_update),
            (self.answer_delete, self.callback_answer_delete),
            (self.answer_back, self.callback_answer_back),
        ]
