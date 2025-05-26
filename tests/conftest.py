"""Configuration for the tests."""

import pytest

from src.core.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Fixture for the application settings."""
    return Settings(
        flight_events_api_url="https://api.flight-events.com",
        max_connections=1,
        max_journey_duration_hours=24,
        max_connextion_duration_hours=4,
    )
