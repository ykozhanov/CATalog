MESSAGE_CREATE_USER_ERROR = "Ошибка при создании нового пользователя"
MESSAGE_GET_TOKEN_ERROR = "Ошибка получения токена"


class CreateUserError(Exception):

    def __init__(self, message: str = MESSAGE_CREATE_USER_ERROR):
        self._message = message
        super().__init__(self._message)