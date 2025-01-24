from dataclasses import dataclass


@dataclass
class KeyboardActionsByElement:
    page: int
    element_id: int

    UPDATE_PREFIX = "update"
    DELETE_PREFIX = "delete"
    USE_PREFIX = "use"
    LIST_PREFIX = "list"
    BACK_PREFIX = "back"

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
    def answer_list(self) -> str:
        return "Товары"

    @property
    def answer_back(self) -> str:
        return "Назад"

    @property
    def callback_answer_update(self) -> str:
        return f"{self.UPDATE_PREFIX}#{self.element_id}"

    @property
    def callback_answer_delete(self) -> str:
        return f"{self.DELETE_PREFIX}#{self.element_id}"

    @property
    def callback_answer_use(self) -> str:
        return f"{self.USE_PREFIX}#{self.element_id}"

    @property
    def callback_answer_list(self) -> str:
        return f"{self.LIST_PREFIX}#{self.element_id}"

    @property
    def callback_answer_back(self) -> str:
        return f"{self.BACK_PREFIX}#{self.page}"

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
