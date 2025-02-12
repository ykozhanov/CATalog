from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_hostname_ns: str
    redis_port_ns: int
    redis_db_ns: int
    redis_password_ns: str | None = None

    def redis_url(self) -> str:
        if self.redis_password_ns is not None:
            return f"redis://:{self.redis_password_ns}@{self.redis_hostname_ns}:{self.redis_port_ns}/{self.redis_db_ns}"
        return f"redis://{self.redis_hostname_ns}:{self.redis_port_ns}/{self.redis_db_ns}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
