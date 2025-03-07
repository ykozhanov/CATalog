from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.backend.core.database.models import Base

if TYPE_CHECKING:
    from src.backend.api.api_v1.products.models import Product

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        order_by="Product.exp_date, null()",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("name", "profile_id", name="uq_category_name_profile"),
    )
