"""Flight events repository that uses an external API."""

import httpx

from src.core.config import Settings
from src.models import FlightEvent

from .exceptions import FlightEventRetrievalError
from .interface import FlightEventReadRepositoryInterface


class FlightEventsAPIRepository(FlightEventReadRepositoryInterface):
    """Flight events repository implementation."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the flight events repository."""
        self.base_url = settings.flight_events_api_url

    async def list(self) -> list[FlightEvent]:
        """List flight events."""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url)

            if response.is_error:
                raise FlightEventRetrievalError(
                    f"Failed to retrieve flight events from API: {response.status_code}"
                )

            return [
                FlightEvent(
                    flight_number=event["flight_number"],
                    from_airport=event["departure_city"],
                    to_airport=event["arrival_city"],
                    departure_time=event["departure_datetime"],
                    arrival_time=event["arrival_datetime"],
                )
                for event in response.json()
            ]
