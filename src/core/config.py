"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    flight_events_api_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")