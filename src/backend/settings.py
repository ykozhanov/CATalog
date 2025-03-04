import os
from typing import Any

from flask import Blueprint
from dotenv import load_dotenv
load_dotenv()

from src.backend.core.database.models import User
from src.backend.api.api_v1.auth.models import Profile
from src.backend.api.api_v1 import categories_bp, auth_bp, products_bp


def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=host if host else os.getenv("POSTGRES_HOST"),
        port=port if port else os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("DB_NAME_BACKEND"),
    )


COMMON_PREFIX = "/api/v1"

BPS: list[dict[str, Blueprint | Any]] = [
    {"blueprint": auth_bp, "url_prefix": f"{COMMON_PREFIX}/auth"},
    {"blueprint": products_bp, "url_prefix": f"{COMMON_PREFIX}/products"},
    {"categories": categories_bp, "url_prefix": f"{COMMON_PREFIX}/categories"},
]

USER_MODEL = User
PROFILE_MODEL = Profile
