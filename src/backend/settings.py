# import os
from typing import Any

from flask import Blueprint

# from src.backend.core.database.models import User
# from src.backend.api.api_v1.auth.models import Profile
# from src.backend.api.api_v1 import categories_bp, auth_bp, products_bp


# def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
#     return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
#         username=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=host if host else os.getenv("POSTGRES_HOST"),
#         port=port if port else os.getenv("POSTGRES_PORT"),
#         dbname=os.getenv("DB_NAME_BACKEND"),
#     )


# COMMON_PREFIX = "/api/v1"
#
# def get_bps() -> list[dict[str, Blueprint | Any]]:
#     from src.backend.api.api_v1 import categories_bp, auth_bp, products_bp
#     return [
#     {"blueprint": auth_bp, "url_prefix": f"{COMMON_PREFIX}/auth"},
#     {"blueprint": products_bp, "url_prefix": f"{COMMON_PREFIX}/products"},
#     {"categories": categories_bp, "url_prefix": f"{COMMON_PREFIX}/categories"},
# ]

# BPS = get_bps()
#
# USER_MODEL = User
# PROFILE_MODEL = Profile
#
# def get_user_model():
#     from src.backend.core.database.models import User
#     return User
#
# def get_profile_model():
#     from src.backend.api.api_v1.auth.models import Profile
#     return Profile

# USER_MODEL = get_user_model()
# PROFILE_MODEL = get_profile_model()
#
# def get_profile_model():
#     from src.backend.api.api_v1.auth.models import Profile
#     return Profile
#
# BPS = get_bps()

# USER_MODEL = User

# PROFILE_MODEL = get_profile_model()
