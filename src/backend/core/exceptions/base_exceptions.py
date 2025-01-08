from .messages import MESSAGE_AUTHENTICATION_ERROR_401, MESSAGE_FORBIDDEN_ERROR_403, MESSAGE_ENV_ERROR


class ENVError(Exception):

    def __init__(self, message: str = MESSAGE_ENV_ERROR):
        self.message = message
        super().__init__(message)


class AuthenticationError(Exception):

    def __init__(self, message: str = MESSAGE_AUTHENTICATION_ERROR_401):
        self.message = message
        super().__init__(message)


class ForbiddenError(Exception):

    def __init__(self, message: str = MESSAGE_FORBIDDEN_ERROR_403):
        self.message = message
        super().__init__(message)
