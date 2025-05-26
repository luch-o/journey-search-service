"""Dependencies for the application."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.core.config import Settings


@lru_cache
def get_settings() -> Settings:
    """Get the settings."""
    return Settings()


AppSettings = Annotated[Settings, Depends(get_settings)]
