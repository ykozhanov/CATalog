from src.db_lib.base.exceptions import IntegrityDBError

from src.frontend.telegram.core.utils import crud
from src.frontend.telegram.core.database.models import User
from src.frontend.telegram.core.exceptions import CreateUserError
from src.frontend.telegram.core.exceptions.messages import MESSAGE_CREATE_USER_ERROR

from .schemas import UserInSchema


class UserController:

    def __init__(self, telegram_user_id: int):
        self._telegram_user_id = telegram_user_id

    def add_user(self, user_in_schema: UserInSchema) -> User:
        try:
            new_user = User(telegram_user_id=self._telegram_user_id, **user_in_schema.model_dump())
        except IntegrityDBError as e:
            raise CreateUserError(f"{MESSAGE_CREATE_USER_ERROR}: {str(e)}")
        else:
            return crud.create(new_user)

    def get_user(self) -> User:
        return crud.read(User, self._telegram_user_id)

    def delete_user(self) -> None:
        crud.delete(User, self._telegram_user_id)
