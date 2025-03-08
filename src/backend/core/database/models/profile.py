from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.backend.core.database.models import Base, User

if TYPE_CHECKING:
    from src.backend.api.api_v1.categories.models import Category
    from src.backend.api.api_v1.products.models import Product


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    user: Mapped[User] = relationship(
        "User",
        back_populates="profile",
        lazy="joined",
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        backref="profile",
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        backref="profile",
        lazy="subquery",
        cascade="all, delete-orphan",
    )
