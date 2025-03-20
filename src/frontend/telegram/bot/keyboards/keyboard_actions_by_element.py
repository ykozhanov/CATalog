class KeyboardActionsByElement:
    EDIT_PREFIX = "edit"
    DELETE_PREFIX = "delete"
    BACK_PREFIX = "back"

    USE_PREFIX = "use"
    LIST_PREFIX = "list"

    def __init__(self, page: int, element_index: int):
        self._page = page
        self._element_index = element_index


    @classmethod
    def answer_edit(cls) -> str:
        return "Изменить 🔄"

    @classmethod
    def answer_delete(cls) -> str:
        return "Удалить 🗑"

    @classmethod
    def answer_use(cls) -> str:
        return "Использовать ✅"

    @classmethod
    def answer_list(cls) -> str:
        return "Товары 🍱"

    @classmethod
    def answer_back(cls) -> str:
        return "⏮️ Назад"

    @property
    def callback_answer_edit(self) -> str:
        return f"{self.EDIT_PREFIX}#{self._element_index}"

    @property
    def callback_answer_delete(self) -> str:
        return f"{self.DELETE_PREFIX}#{self._element_index}"

    @property
    def callback_answer_use(self) -> str:
        return f"{self.USE_PREFIX}#{self._element_index}"

    @property
    def callback_answer_list(self) -> str:
        return f"{self.LIST_PREFIX}#{self._element_index}"

    @property
    def callback_answer_back(self) -> str:
        return f"{self.BACK_PREFIX}#{self._page}"

    def get_inline_keyboard_product(self) -> list[tuple[str, str]]:
        return [
            (self.answer_use(), self.callback_answer_use),
            (self.answer_edit(), self.callback_answer_edit),
            (self.answer_delete(), self.callback_answer_delete),
            (self.answer_back(), self.callback_answer_back),
        ]

    def get_inline_keyboard_category(self) -> list[tuple[str, str]]:
        return [
            (self.answer_list(), self.callback_answer_list),
            (self.answer_edit(), self.callback_answer_edit),
            (self.answer_delete(), self.callback_answer_delete),
            (self.answer_back(), self.callback_answer_back),
        ]
