from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.backend.core.database.models import Base

from src.backend.api.api_v1.products.models import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)

    products: Mapped[list[Product]] = relationship(
        Product,
        back_populates="category",
        order_by="Product.exp_date, Product.exp_date is NULL",
    )
