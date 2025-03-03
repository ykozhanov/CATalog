import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    db_username: str
    db_password: str
    db_name_notification_service: str
    db_host: str
    db_port: str
    backend_url: str
    exp_days: int
    token_crypt_key: bytes

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class KafkaSettings(BaseSettings):
    topic_name_new_telegram_user = "new_telegram_user"
    topic_name_delete_telegram_user = "delete_telegram_user"
    bootstrap_servers = "kafka:9092"
    kafka_username = os.getenv("KAFKA_USERNAME")
    kafka_password = os.getenv("KAFKA_PASSWORD")


def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
        username=Settings.db_username,
        password=Settings.db_password,
        host=host if host else Settings.db_host,
        port=port if port else Settings.db_port,
        dbname=Settings.db_name_notification_service,
    )


settings = Settings()