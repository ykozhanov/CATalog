from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    telegram_user_id: int
    telegram_chat_id: int
    refresh_jtw_token: str
