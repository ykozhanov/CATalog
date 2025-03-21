from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    telegram_user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_chat_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    refresh_jtw_token: Mapped[str] = mapped_column(String, nullable=False)

    def __str__(self) -> str:
        return str(f"User {self.telegram_user_id}")
