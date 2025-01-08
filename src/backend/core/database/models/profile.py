from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.backend.core.database.models import Base
from src.backend.settings import USER_MODEL


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    user: Mapped[USER_MODEL] = relationship(
        USER_MODEL,
        back_populates="profile",
        lazy="joined",
        cascade="all, delete-orphan",
    )
