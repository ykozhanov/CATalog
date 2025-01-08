from .messages import MESSAGE_NOT_FOUND_IN_DB_ERROR


class NotFoundInDBError(Exception):

    def __init__(self, message: str = MESSAGE_NOT_FOUND_IN_DB_ERROR):
        self.message = message
        super().__init__(self.message)
