from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.settings import PROFILE_MODEL
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(length=150), nullable=False)

    profile: Mapped[PROFILE_MODEL] = relationship(PROFILE_MODEL, back_populates="profile", lazy="joined")

    def __str__(self) -> str:
        return self.__class__.__name__
