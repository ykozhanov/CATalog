from .messages import MESSAGE_AUTHENTICATION_ERROR_401, MESSAGE_FORBIDDEN_ERROR_403, MESSAGE_ENV_ERROR, MESSAGE_BAD_REQUEST_ERROR_400


class ENVError(Exception):

    def __init__(self, message: str = MESSAGE_ENV_ERROR):
        self._message = message
        super().__init__(self._message)


class AuthenticationError(Exception):

    def __init__(self, message: str = MESSAGE_AUTHENTICATION_ERROR_401):
        self._message = message
        super().__init__(self._message)


class ForbiddenError(Exception):

    def __init__(self, message: str = MESSAGE_FORBIDDEN_ERROR_403):
        self._message = message
        super().__init__(self._message)


class BadRequestError(Exception):

    def __init__(self, message: str = MESSAGE_BAD_REQUEST_ERROR_400):
        self._message = message
        super().__init__(self._message)
