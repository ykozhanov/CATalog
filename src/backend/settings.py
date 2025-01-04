from .app import app
from .routes import users_bp, products_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
