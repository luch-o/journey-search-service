"""Test the search journeys endpoint."""

from collections.abc import Generator
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.core.config import Settings
from src.core.dependencies import get_settings
from src.main import app
from src.models import FlightEvent, Journey
from src.repositories.flight_events import FlightEventRetrievalError


@pytest.fixture(name="client")
def client_fixture(settings: Settings) -> Generator[TestClient, None, None]:
    """Get a test client for the application."""

    def get_settings_override() -> Generator[Settings, None, None]:
        """Override the session dependency."""
        yield settings

    app.dependency_overrides[get_settings] = get_settings_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestSearchJourneys:
    """Test the GET /journeys/search endpoint."""

    @patch(
        "src.commands.SearchJourneysCommand.execute",
        AsyncMock(
            return_value=[
                Journey(
                    path=[
                        FlightEvent(
                            flight_number="XX1234",
                            from_airport="BUE",
                            to_airport="MAD",
                            departure_time=datetime(2024, 9, 12, 10, 0, 0),
                            arrival_time=datetime(2024, 9, 12, 11, 0, 0),
                        ),
                    ],
                ),
            ]
        ),
    )
    async def test_search_success(self, client: TestClient) -> None:
        """Test the search journeys endpoint."""
        response = client.get("/journeys/search?date=2024-09-12&from=BUE&to=MAD")
        assert response.status_code == 200
        assert response.json() == [
            {
                "connections": 0,
                "path": [
                    {
                        "flight_number": "XX1234",
                        "from": "BUE",
                        "to": "MAD",
                        "departure_time": "2024-09-12 10:00:00",
                        "arrival_time": "2024-09-12 11:00:00",
                    }
                ],
            }
        ]

    @patch(
        "src.commands.SearchJourneysCommand.execute",
        AsyncMock(
            side_effect=FlightEventRetrievalError("Failed to retrieve flight events")
        ),
    )
    async def test_search_fails_retrieval_error(self, client: TestClient) -> None:
        """Test the search journeys endpoint fails if the retrieval error is raised."""
        response = client.get("/journeys/search?date=2025-05-25&from=LON&to=PAR")
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to retrieve flight events"}
