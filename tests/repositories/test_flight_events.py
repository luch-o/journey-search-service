"""Test the flight events API."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.config import Settings
from src.models import FlightEvent
from src.repositories.flight_events.exceptions import FlightEventRetrievalError
from src.repositories.flight_events.main import FlightEventsAPIRepository


@pytest.mark.asyncio
class TestFlightEventsAPI:
    """Test the flight events API."""

    @pytest.fixture
    def repository(self, settings: Settings) -> FlightEventsAPIRepository:
        """Fixture for the repository."""
        return FlightEventsAPIRepository(settings)

    @patch(
        "httpx.AsyncClient.get",
        AsyncMock(
            **{
                "return_value": MagicMock(
                    **{
                        "is_error": False,
                        "status_code": 200,
                        "json.return_value": [
                            {
                                "flight_number": "IB1234",
                                "departure_city": "MAD",
                                "arrival_city": "BUE",
                                "departure_datetime": "2021-12-31T23:59:59.000Z",
                                "arrival_datetime": "2022-01-01T12:00:00.000Z",
                            },
                            {
                                "flight_number": "IB2345",
                                "departure_city": "MAD",
                                "arrival_city": "VLC",
                                "departure_datetime": "2022-01-01T17:00:00.000Z",
                                "arrival_datetime": "2022-01-02T18:00:00.000Z",
                            },
                        ],
                    }
                )
            }
        ),
    )
    async def test_flight_events_api_list(
        self, repository: FlightEventsAPIRepository
    ) -> None:
        """Test the flight events API list method."""
        flight_events = await repository.list()
        assert flight_events == [
            FlightEvent(
                flight_number="IB1234",
                from_airport="MAD",
                to_airport="BUE",
                departure_time="2021-12-31T23:59:59.000Z",
                arrival_time="2022-01-01T12:00:00.000Z",
            ),
            FlightEvent(
                flight_number="IB2345",
                from_airport="MAD",
                to_airport="VLC",
                departure_time="2022-01-01T17:00:00.000Z",
                arrival_time="2022-01-02T18:00:00.000Z",
            ),
        ]

    @patch(
        "httpx.AsyncClient.get",
        AsyncMock(
            **{
                "return_value": AsyncMock(
                    **{
                        "is_error": True,
                        "status_code": 500,
                        "json.return_value": {"message": "Internal server error"},
                    }
                )
            }
        ),
    )
    async def test_flight_events_api_list_error(
        self, repository: FlightEventsAPIRepository
    ) -> None:
        """Test the flight events API list method with an error."""
        with pytest.raises(FlightEventRetrievalError):
            await repository.list()
