from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(length=100), unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(length=150), nullable=False)

    profile: Mapped[Profile] = relationship(
        "Profile",
        back_populates="profile",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    def __str__(self) -> str:
        return self.__class__.__name__
