# from sqlalchemy.orm import relationship, Mapped
#
# from src.backend.core.database.models import Profile as BaseProfile

# from src.backend.api.api_v1.categories.models import Category
# from src.backend.api.api_v1.products.models import Product

#
# class Profile(BaseProfile):
#
#     products: Mapped[list[Product]] = relationship("Product", back_populates="profile", lazy="subquery")
#     categories: Mapped[list[Category]] = relationship("Category", back_populates="profile", lazy="subquery")
