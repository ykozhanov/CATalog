from .messages import MESSAGE_NOT_FOUND_IN_DB_ERROR, MESSAGE_BAD_REQUEST_DB


class NotFoundInDBError(Exception):

    def __init__(self, message: str = MESSAGE_NOT_FOUND_IN_DB_ERROR):
        self._message = message
        super().__init__(self._message)


class BadRequestDBError(Exception):
    def __init__(self, message: str = MESSAGE_BAD_REQUEST_DB):
        self._message = message
        super().__init__(self._message)
