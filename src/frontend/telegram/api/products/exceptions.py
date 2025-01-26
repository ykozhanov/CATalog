MESSAGE_PRODUCT_ERROR = "Ошибка при работе с продуктами"


class ProductError(Exception):

    def __init__(self, message: str = MESSAGE_PRODUCT_ERROR):
        self._message = message
        super().__init__(self._message)