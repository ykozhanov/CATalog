import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_hostname: str
    redis_port: int
    redis_db: int
    redis_password: str | None

    def redis_url(self) -> str:
        if self.redis_password is not None:
            return f"redis://:{self.redis_password}@{self.redis_hostname}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_hostname}:{self.redis_port}/{self.redis_db}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
