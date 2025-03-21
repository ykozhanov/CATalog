from cryptography.fernet import Fernet

from .models import TelegramUser
from .schemas import TelegramUserSchema
from .crud_util import crud, session as S

from src.notification_service.telegram.settings import settings


def decrypt_user_data(user_data: TelegramUserSchema) -> TelegramUserSchema:
    ciper = Fernet(settings.token_crypt_key)
    token_encrypt = user_data.refresh_jtw_token
    user_data.refresh_jtw_token = ciper.decrypt(token_encrypt.encode("utf-8")).decode("utf-8")
    return user_data


class TelegramUserController:
    @staticmethod
    def create_or_update_user(user_data: TelegramUserSchema) -> None:
        try:
            decrypt_ud = decrypt_user_data(user_data)
            if crud.read(TelegramUser, (user_data.telegram_user_id, user_data.telegram_chat_id)):

                crud.update(
                    model=TelegramUser,
                    pk=(user_data.telegram_user_id, user_data.telegram_chat_id),
                    obj_data=decrypt_ud.model_dump(),
                )
            else:
                user = TelegramUser(**decrypt_ud.model_dump())
                crud.create(user)
        except Exception as e:
            print(str(e))

    @staticmethod
    def delete_user(user_data: TelegramUserSchema) -> None:
        session = S.session()
        with session as s:
            user = s.query(TelegramUser).filter(
                TelegramUser.telegram_user_id == user_data.telegram_user_id,
                TelegramUser.telegram_chat_id == user_data.telegram_chat_id,
            ).first()
            if user:
                s.delete(user)
                s.commit()

    @staticmethod
    def read_all() -> list[TelegramUser]:
        return crud.read_all(TelegramUser)
