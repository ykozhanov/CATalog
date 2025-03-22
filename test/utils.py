import base64

from enum import Enum
from test.models import Credential


class APIPathsEnum(Enum):
    REGISTER = "/api/v1/auth/register/"
    LOGIN = "/api/v1/auth/login/"
    TOKEN = "/api/v1/auth/token/"
    CATEGORIES = "/api/v1/categories/"
    PRODUCTS = "/api/v1/products/"


def register_credential_base64_encode(credential: Credential) -> str:
    credential_bytes = f"{credential.username}:{credential.password}:{credential.email}".encode("utf-8")
    return base64.b64encode(credential_bytes).decode("utf-8")


def login_credential_base64_encode(credential: Credential) -> str:
    credential_bytes = f"{credential.username}:{credential.password}".encode("utf-8")
    return base64.b64encode(credential_bytes).decode("utf-8")


def set_basic_token_prefix(credential: str) -> str:
    return f"Basic {credential}"


def set_bearer_token_prefix(credential: str) -> str:
    return f"Bearer {credential}"
