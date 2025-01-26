class KeyboardYesOrNo:

    @property
    def answer_yes(self) -> str:
        return "Да"

    @property
    def answer_no(self) -> str:
        return "Нет"

    @property
    def callback_answer_yes(self) -> str:
        return "answer#yes"

    @property
    def callback_answer_no(self) -> str:
        return "answer#no"

    def get_inline_keyboard(self) -> list[tuple[str, str]]:
        return [
            (self.answer_yes, self.callback_answer_yes),
            (self.answer_no, self.callback_answer_no),
        ]
