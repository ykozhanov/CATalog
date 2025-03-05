from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import date

from sqlalchemy import Integer, String, CheckConstraint, Date, func, ForeignKey, Float, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy.engine import Connection

from src.backend.core.database.models import Base

# from src.backend.settings import PROFILE_MODEL
# from src.backend.api.api_v1.categories.models import Category

if TYPE_CHECKING:
    from src.backend.core.database.models import Profile
    from src.backend.api.api_v1.categories.models import Category

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String(length=10), nullable=False, default="шт.")
    quantity: Mapped[float] = mapped_column(Float, CheckConstraint("quantity >= 0"), nullable=False, default=1)
    exp_date: Mapped[date] = mapped_column(Date)
    note: Mapped[str] = mapped_column(String(length=500))
    created_at: Mapped[date] = mapped_column(Date, default=func.current_date)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="products", lazy="joined")
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="products",
        lazy="joined",
        cascade="all, delete-orphan",
    )


def delete_product_if_quantity_zero(mapper: Mapper, connection: Connection, target: Product):
    if target.quantity <= 0:
        connection.execute(Product.__table__.delete().where(Product.id == target.id))

event.listen(Product, "after_update", delete_product_if_quantity_zero)
