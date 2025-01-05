import os
from typing import Any

from flask import Blueprint
from dotenv import load_dotenv
load_dotenv()

from .core.settings.database import User
from .categories.routes import categories_bp
from .auth.routes import auth_bp
from .products.routes import products_bp

BPS: list[dict[str, Blueprint | Any]] = [
    {"blueprint": auth_bp, "url_prefix": "/auth"},
    {"blueprint": products_bp, "url_prefix": "/products"},
    {"categories": categories_bp, "url_prefix": "/categories"},
]

DB_PATH = "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
    username=os.getenv("DB_USERNAME_BACKEND"),
    password=os.getenv("DB_PASSWORD_BACKEND"),
    host=os.getenv("DB_NAME_BACKEND"),
    port=os.getenv("DB_HOST_BACKEND"),
    dbname=os.getenv("DB_PORT_BACKEND"),
)

SUB_PAYLOAD_JWT = "sub"

USER_MODEL = User

AUTH_HEADER = "Authorization"
