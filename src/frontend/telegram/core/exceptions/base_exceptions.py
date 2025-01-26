from .messages import (
    MESSAGE_ENV_ERROR,
    MESSAGE_AUTHENTICATION_ERROR,
    MESSAGE_CREATE_MESSAGE_ERROR,
)


class ENVError(Exception):

    def __init__(self, message: str = MESSAGE_ENV_ERROR):
        self._message = message
        super().__init__(self._message)


class CreateMessageError(Exception):

    def __init__(self, message: str = MESSAGE_CREATE_MESSAGE_ERROR):
        self._message = message
        super().__init__(self._message)


class AuthenticationError(Exception):

    def __init__(self, message: str = MESSAGE_AUTHENTICATION_ERROR):
        self._message = message
        super().__init__(self._message)
