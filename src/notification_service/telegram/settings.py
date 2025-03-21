from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    postgres_user: str
    postgres_password: str
    db_name_notification_service: str
    postgres_host: str
    postgres_port: str
    backend_url: str = "http://localhost:8000/api"
    exp_days: int
    token_crypt_key: bytes
    notification_hour_utc: str = "14"   # По умолчанию 19:00 по Екатеринбургу
    notification_minutes_utc: str = "0"

    @field_validator("token_crypt_key", mode="before")
    def convert_to_bytes(cls, value: str) -> bytes:
        return value.encode("utf-8")

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class KafkaSettings(BaseSettings):
    topic_name_new_telegram_user: str = "new_telegram_user"
    topic_name_delete_telegram_user: str = "delete_telegram_user"
    bootstrap_servers: str = "kafka:9092"
    kafka_username: str
    kafka_password: str

    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
kafka_settings = KafkaSettings()


def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
        username=settings.postgres_user,
        password=settings.postgres_password,
        host=host if host else settings.postgres_host,
        port=port if port else settings.postgres_port,
        dbname=settings.db_name_notification_service,
    )
