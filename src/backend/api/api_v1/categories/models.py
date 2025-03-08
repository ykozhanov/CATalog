from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, case
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.backend.core.database.models import Base
from src.backend.api.api_v1.products.models import Product

# if TYPE_CHECKING:
#     pass

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        order_by=(
            case(
                (Product.exp_date.isnot(None), 1),
                else_=0,
            ),
            Product.exp_date,
        ),
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("name", "profile_id", name="uq_category_name_profile"),
    )
