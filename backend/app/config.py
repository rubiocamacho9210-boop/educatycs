"""
Configuration management using environment variables.
"""

from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///db.sqlite3"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # CORS
    allowed_origins: str = "*"

    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_window_seconds: int = 60

    # Scheduler
    scheduler_interval_hours: int = 6

    # Admin
    admin_api_key: str = ""

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
