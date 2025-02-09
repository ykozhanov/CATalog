MESSAGE_GET_TOKEN_ERROR = "Ошибка получения токена"
MESSAGE_AUTHENTICATION_ERROR = "Ошибка аутентификации"


class AuthenticationError(Exception):

    def __init__(self, message: str = MESSAGE_AUTHENTICATION_ERROR):
        self._message = message
        super().__init__(self._message)


class GetTokenError(Exception):

    def __init__(self, message: str = MESSAGE_GET_TOKEN_ERROR):
        self._message = message
        super().__init__(self._message)