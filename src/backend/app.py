from typing import Any

from flask import Flask, Blueprint

from src.backend.api.api_v1 import categories_bp, auth_bp, products_bp
from src.backend.settings import COMMON_PREFIX

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix=f"{COMMON_PREFIX}/auth")
app.register_blueprint(products_bp, url_prefix=f"{COMMON_PREFIX}/products")
app.register_blueprint(categories_bp, url_prefix=f"{COMMON_PREFIX}/categories")
