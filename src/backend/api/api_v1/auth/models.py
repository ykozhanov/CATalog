from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, mapped_collection

from src.backend.core.database.models import Base
from src.backend.settings import USER_MODEL


class JWTTokens(Base):
    __tablename__ = 'jwt_tokens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    user: Mapped[USER_MODEL] = relationship(USER_MODEL, backref="jwt_token", lazy="joined", cascade="all, delete-orphan")
