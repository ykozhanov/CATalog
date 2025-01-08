import os
from typing import Any

from flask import Blueprint
from dotenv import load_dotenv
load_dotenv()

from .core.database.models import User
from .api.api_v1 import categories_bp, auth_bp, products_bp

COMMON_PREFIX = "/api"


BPS: list[dict[str, Blueprint | Any]] = [
    {"blueprint": auth_bp, "url_prefix": f"{COMMON_PREFIX}/auth"},
    {"blueprint": products_bp, "url_prefix": f"{COMMON_PREFIX}/products"},
    {"categories": categories_bp, "url_prefix": f"{COMMON_PREFIX}/categories"},
]

DB_PATH = "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
    username=os.getenv("DB_USERNAME_BACKEND"),
    password=os.getenv("DB_PASSWORD_BACKEND"),
    host=os.getenv("DB_NAME_BACKEND"),
    port=os.getenv("DB_HOST_BACKEND"),
    dbname=os.getenv("DB_PORT_BACKEND"),
)

#TODO Удалить если не надо
    # SUB_PAYLOAD_JWT = "sub"

USER_MODEL = User
