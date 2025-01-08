from datetime import date

from sqlalchemy import Integer, String, CheckConstraint, Date, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.core.database.models import Base

from src.backend.settings import PROFILE_MODEL
from src.backend.api.api_v1.categories.models import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String(length=10), nullable=False, default="шт.")
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity >= 0"), nullable=False, default=0)
    exp_date: Mapped[date] = mapped_column(Date)
    note: Mapped[str] = mapped_column(Text(length=500))
    created_at: Mapped[date] = mapped_column(Date, default=func.current_date)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"))

    category: Mapped[Category] = relationship(Category, back_populates="products", lazy="joined")
    profile: Mapped[PROFILE_MODEL] = relationship(PROFILE_MODEL, back_populates="products", lazy="joined", cascade="all, delete-orphan")
