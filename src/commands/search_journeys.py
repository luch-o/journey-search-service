"""Search journeys command."""

from datetime import date

from src.commands.interface import CommandInterface
from src.models.models import Journey
from src.repositories.flight_events.interface import FlightEventReadRepositoryInterface


class SearchJourneysCommand(CommandInterface):
    """Search journeys command."""

    def __init__(
        self,
        date: date,
        from_airport: str,
        to_airport: str,
        flight_events_repository: FlightEventReadRepositoryInterface,
    ) -> None:
        """Initialize the search journeys command."""
        self.flight_events_repository = flight_events_repository
        self.date = date
        self.from_airport = from_airport
        self.to_airport = to_airport

    async def execute(self) -> list[Journey]:
        """Search journeys for a given date, destination and origin."""
        journeys = []
        flight_events = await self.flight_events_repository.list()
        for flight_event in flight_events:
            if (
                flight_event.from_airport == self.from_airport
                and flight_event.to_airport == self.to_airport
                and flight_event.departure_time.date() == self.date
            ):
                journeys.append(Journey(path=[flight_event]))
        return journeys
