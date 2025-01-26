MESSAGE_CATEGORY_ERROR = "Ошибка при работе с категориями"

class CategoryError(Exception):

    def __init__(self, message: str = MESSAGE_CATEGORY_ERROR):
        self._message = message
        super().__init__(self._message)