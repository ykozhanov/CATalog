from .messages import (
    MESSAGE_ENV_ERROR,
    MESSAGE_CREATE_MESSAGE_ERROR,
    MESSAGE_CREATE_USER_ERROR,
    MESSAGE_AUTHENTICATION_ERROR,
    MESSAGE_GET_TOKEN_ERROR,
    MESSAGE_PRODUCT_ERROR,
    MESSAGE_CATEGORY_ERROR,
)


class ENVError(Exception):

    def __init__(self, message: str = MESSAGE_ENV_ERROR):
        self._message = message
        super().__init__(self._message)


class CreateMessageError(Exception):

    def __init__(self, message: str = MESSAGE_CREATE_MESSAGE_ERROR):
        self._message = message
        super().__init__(self._message)


class CreateUserError(Exception):

    def __init__(self, message: str = MESSAGE_CREATE_USER_ERROR):
        self._message = message
        super().__init__(self._message)


class AuthenticationError(Exception):

    def __init__(self, message: str = MESSAGE_AUTHENTICATION_ERROR):
        self._message = message
        super().__init__(self._message)


class GetTokenError(Exception):

    def __init__(self, message: str = MESSAGE_GET_TOKEN_ERROR):
        self._message = message
        super().__init__(self._message)


class ProductError(Exception):

    def __init__(self, message: str = MESSAGE_PRODUCT_ERROR):
        self._message = message
        super().__init__(self._message)


class CategoryError(Exception):

    def __init__(self, message: str = MESSAGE_CATEGORY_ERROR):
        self._message = message
        super().__init__(self._message)
