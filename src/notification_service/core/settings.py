from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url_notification_service: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
