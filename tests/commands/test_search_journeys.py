"""Test the search journeys command."""

from datetime import date, datetime
from unittest.mock import AsyncMock

import pytest

from src.commands.search_journeys import SearchJourneysCommand
from src.models.models import FlightEvent, Journey


@pytest.mark.asyncio
class TestSearchJourneysCommand:
    """Test the search journeys command."""

    async def test_search_journeys_command_no_events(self) -> None:
        """Test the search journeys command with no flight events.

        If flight events repository returns no events,
        the command should return an empty list.
        """
        flight_events_repository = AsyncMock(**{"list.return_value": []})
        command = SearchJourneysCommand(
            date=date(2021, 12, 31),
            from_airport="MAD",
            to_airport="BUE",
            flight_events_repository=flight_events_repository,
        )
        assert await command.execute() == []

    async def test_search_journeys_command_direct_flight(self) -> None:
        """Test the search journeys command with a direct flight.

        If there is a direct flight, the command should return a journey
        with that flight.
        """
        flight_events_repository = AsyncMock(
            **{
                "list.return_value": [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0),
                    )
                ]
            }
        )
        command = SearchJourneysCommand(
            date=date(2021, 12, 31),
            from_airport="MAD",
            to_airport="BUE",
            flight_events_repository=flight_events_repository,
        )
        assert await command.execute() == [
            Journey(
                path=[
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0),
                    )
                ]
            )
        ]
