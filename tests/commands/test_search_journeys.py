"""Test the search journeys command."""

from datetime import date, datetime
from unittest.mock import AsyncMock

import pytest

from src.commands.search_journeys import SearchJourneysCommand
from src.models.models import FlightEvent, Journey


@pytest.mark.asyncio
class TestSearchJourneysCommand:
    """Test the search journeys command."""

    @pytest.mark.parametrize(
        "flight_events,expected_journeys",
        [
            # Test case 1: No flight events
            pytest.param(
                [],
                [],
                id="no-flight-events",
            ),
            # Test case 2: Direct flight
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0),
                    )
                ],
                [
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
                ],
                id="single-event-direct-flight",
            ),
        ],
    )
    async def test_search_journeys_command(
        self, flight_events: list[FlightEvent], expected_journeys: list[Journey]
    ) -> None:
        """Test the search journeys command with different flight event scenarios.

        Args:
            flight_events: List of flight events to be returned by the repository
            expected_journeys: Expected list of journeys to be returned by the command

        """
        flight_events_repository = AsyncMock(**{"list.return_value": flight_events})
        command = SearchJourneysCommand(
            date=date(2021, 12, 31),
            from_airport="MAD",
            to_airport="BUE",
            flight_events_repository=flight_events_repository,
        )
        assert await command.execute() == expected_journeys
