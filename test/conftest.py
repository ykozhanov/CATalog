import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем путь к src в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Устанавливаем переменную APP_TESTING
os.environ["APP_TESTING"] = "True"

# Подгружаем переменные из .env-test
load_dotenv()

import pytest

from src.backend.app import app as _app
from src.backend.core.database.database_init import engine
from src.backend.api.api_v1.models import Base
from src.backend.core.decorators.base64_login import AUTH_HEADER

from test.utils import login_credential_base64_encode, set_basic_token_prefix, APIPathsEnum
from test.models import JWTTokens, test_user


@pytest.fixture(scope="session", autouse=True)
def app():
    with _app.app_context():
        # Создаем таблицы через импортируемый engine, чтобы использовалась БД из одной области видимости
        Base.metadata.create_all(engine)
        yield _app
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def jwt_tokens(client) -> JWTTokens:
    credential_base64 = login_credential_base64_encode(test_user)
    basic_token = set_basic_token_prefix(credential_base64)

    headers = {AUTH_HEADER: basic_token}
    response = client.post(APIPathsEnum.LOGIN.value, headers=headers)
    response_data: dict = response.json

    response_tokens = JWTTokens(
        access_token=response_data.get("access_token", None),
        refresh_token=response_data.get("refresh_token", None),
    )

    return response_tokens
