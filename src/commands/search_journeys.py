"""Search journeys command."""

from datetime import date, timedelta

from src.commands.interface import CommandInterface
from src.core.config import Settings
from src.models.models import FlightEvent, Journey
from src.repositories.flight_events.interface import FlightEventReadRepositoryInterface


class SearchJourneysCommand(CommandInterface):
    """Search journeys command."""

    def __init__(
        self,
        date: date,
        from_airport: str,
        to_airport: str,
        flight_events_repository: FlightEventReadRepositoryInterface,
        settings: Settings,
    ) -> None:
        """Initialize the search journeys command."""
        self.flight_events_repository = flight_events_repository
        self.date = date
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.settings = settings

    async def execute(self) -> list[Journey]:
        """Search journeys for a given date, destination and origin."""
        flight_events = await self.flight_events_repository.list()
        relevant_events_mapping = self.__get_relevant_flight_events_mapping(
            flight_events
        )
        return self.__find_journeys(relevant_events_mapping)

    def __get_relevant_flight_events_mapping(
        self, flight_events: list[FlightEvent]
    ) -> dict[str, list[FlightEvent]]:
        """Get a mapping of relevant flight events.

        A flight event is relevant if its date and arrival dates are within the
        search date plus settings.max_journey_duration_hours.

        Args:
            flight_events: List of flight events to be mapped

        Returns:
            A mapping of relevant flight events that could be used to build a journey.
            The key is the departure city, and the value is a list of flight events
            departing from that city.

        """
        relevant = {}
        max_arrival_date = self.date + timedelta(
            hours=self.settings.max_journey_duration_hours
        )
        for flight_event in flight_events:
            if self.date <= flight_event.departure_time.date() <= max_arrival_date:
                if flight_event.from_airport not in relevant:
                    relevant[flight_event.from_airport] = []
                relevant[flight_event.from_airport].append(flight_event)
        return relevant

    def __find_journeys(
        self, relevant_events_mapping: dict[str, list[FlightEvent]]
    ) -> list[Journey]:
        """Get journeys from a mapping of relevant flight events."""
        journeys = []
        for flight_event in relevant_events_mapping.get(self.from_airport, []):
            if flight_event.to_airport == self.to_airport:
                journeys.append(Journey(path=[flight_event]))
            else:
                paths = self.__find_paths(
                    flight_event.to_airport,
                    [flight_event],
                    relevant_events_mapping,
                )
                for path in paths:
                    journeys.append(Journey(path=path))
        return journeys

    def __find_paths(
        self,
        from_airport: str,
        path: list[FlightEvent],
        relevant_events_mapping: dict[str, list[FlightEvent]],
    ) -> list[FlightEvent]:
        """Find valid paths from a given airport to the destination airport.

        Args:
            from_airport: The airport to start from
            path: The current path of flight events
            relevant_events_mapping: A mapping of relevant flight events

        Returns:
            A list of valid paths from the given airport to the destination airport

        """
        paths = []
        for flight_event in relevant_events_mapping[from_airport]:
            if len(path) > self.settings.max_connections:
                break
            if flight_event.to_airport == self.to_airport:
                paths.append(path + [flight_event])
            else:
                paths.extend(
                    self.__find_paths(
                        flight_event.to_airport,
                        path + [flight_event],
                        relevant_events_mapping,
                    )
                )
        return paths
