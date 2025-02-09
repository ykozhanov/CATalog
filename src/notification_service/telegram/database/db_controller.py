from .models import TelegramUser
from .schemas import TelegramUserSchema
from .crud_util import crud


class TelegramUserController:

    @staticmethod
    def create_or_update_user(user_data: TelegramUserSchema) -> None:
        if crud.read(TelegramUser, (user_data.telegram_user_id, user_data.telegram_chat_id)):
            crud.update(
                model=TelegramUser,
                pk=(user_data.telegram_user_id, user_data.telegram_chat_id),
                obj_data=user_data.model_dump(),
            )
        else:
            user = TelegramUser(**user_data.model_dump())
            crud.create(user)

    @staticmethod
    def delete_user(user_data: TelegramUserSchema) -> None:
        if user := crud.read(TelegramUser, (user_data.telegram_user_id, user_data.telegram_chat_id)):
            crud.delete(user)

    @staticmethod
    def read_all() -> list[TelegramUser]:
        return crud.read_all(TelegramUser)
