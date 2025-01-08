from .products.routes import products_bp
from .categories.routes import categories_bp
from .auth.routes import auth_bp

__all__ = ["products_bp", "categories_bp", "auth_bp"]
