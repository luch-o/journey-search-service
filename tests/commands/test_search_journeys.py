"""Test the search journeys command."""

from datetime import UTC, date, datetime
from unittest.mock import AsyncMock

import pytest

from src.commands.search_journeys import SearchJourneysCommand
from src.core.config import Settings
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
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0, tzinfo=UTC),
                    )
                ],
                [
                    Journey(
                        path=[
                            FlightEvent(
                                flight_number="IB1234",
                                from_airport="MAD",
                                to_airport="BUE",
                                departure_time=datetime(
                                    2021, 12, 31, 10, 0, 0, tzinfo=UTC
                                ),
                                arrival_time=datetime(
                                    2021, 12, 31, 12, 0, 0, tzinfo=UTC
                                ),
                            )
                        ]
                    )
                ],
                id="single-event-direct-flight",
            ),
            # Test case 3: One direct flight with multiple events
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1235",
                        from_airport="BUE",
                        to_airport="MAD",
                        departure_time=datetime(2021, 12, 31, 13, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 15, 0, 0, tzinfo=UTC),
                    ),
                ],
                [
                    Journey(
                        path=[
                            FlightEvent(
                                flight_number="IB1234",
                                from_airport="MAD",
                                to_airport="BUE",
                                departure_time=datetime(
                                    2021, 12, 31, 10, 0, 0, tzinfo=UTC
                                ),
                                arrival_time=datetime(
                                    2021, 12, 31, 12, 0, 0, tzinfo=UTC
                                ),
                            ),
                        ]
                    )
                ],
                id="one-direct-flight-with-multiple-events",
            ),
            # Test case 4: journey with one connection
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BOG",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1235",
                        from_airport="BOG",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 13, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 15, 0, 0, tzinfo=UTC),
                    ),
                ],
                [
                    Journey(
                        path=[
                            FlightEvent(
                                flight_number="IB1234",
                                from_airport="MAD",
                                to_airport="BOG",
                                departure_time=datetime(
                                    2021, 12, 31, 10, 0, 0, tzinfo=UTC
                                ),
                                arrival_time=datetime(
                                    2021, 12, 31, 12, 0, 0, tzinfo=UTC
                                ),
                            ),
                            FlightEvent(
                                flight_number="IB1235",
                                from_airport="BOG",
                                to_airport="BUE",
                                departure_time=datetime(
                                    2021, 12, 31, 13, 0, 0, tzinfo=UTC
                                ),
                                arrival_time=datetime(
                                    2021, 12, 31, 15, 0, 0, tzinfo=UTC
                                ),
                            ),
                        ]
                    )
                ],
                id="journey-with-one-connection",
            ),
            # Test case 5: discard journey with more than one connection
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BOG",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1235",
                        from_airport="BOG",
                        to_airport="GRU",
                        departure_time=datetime(2021, 12, 31, 13, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 15, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1236",
                        from_airport="GRU",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 16, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 18, 0, 0, tzinfo=UTC),
                    ),
                ],
                [],
                id="discard-many-connections",
            ),
            # Test case 6: discard journey with a connection longer than 4 hours
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BOG",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 12, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1235",
                        from_airport="BOG",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 19, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 23, 0, 0, tzinfo=UTC),
                    ),
                ],
                [],
                id="discard-long-connection-wait",
            ),
            # Test case 7: discard too long journey
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BOG",
                        departure_time=datetime(2021, 12, 31, 10, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2021, 12, 31, 18, 0, 0, tzinfo=UTC),
                    ),
                    FlightEvent(
                        flight_number="IB1235",
                        from_airport="BOG",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 22, 0, 0, tzinfo=UTC),
                        arrival_time=datetime(2022, 1, 1, 11, 30, 0, tzinfo=UTC),
                    ),
                ],
                [],
                id="discard-too-long-journey",
            ),
            # Test case 8: journey at the end of the day
            pytest.param(
                [
                    FlightEvent(
                        flight_number="IB1234",
                        from_airport="MAD",
                        to_airport="BUE",
                        departure_time=datetime(2021, 12, 31, 23, 59, 59, tzinfo=UTC),
                        arrival_time=datetime(2022, 1, 1, 12, 0, 0, tzinfo=UTC),
                    ),
                ],
                [
                    Journey(
                        path=[
                            FlightEvent(
                                flight_number="IB1234",
                                from_airport="MAD",
                                to_airport="BUE",
                                departure_time=datetime(
                                    2021, 12, 31, 23, 59, 59, tzinfo=UTC
                                ),
                                arrival_time=datetime(2022, 1, 1, 12, 0, 0, tzinfo=UTC),
                            ),
                        ]
                    )
                ],
                id="journey-at-the-end-of-the-day",
            ),
        ],
    )
    async def test_search_journeys_command(
        self,
        flight_events: list[FlightEvent],
        expected_journeys: list[Journey],
        settings: Settings,
    ) -> None:
        """Test the search journeys command with different flight event scenarios.

        Args:
            flight_events: List of flight events to be returned by the repository
            expected_journeys: Expected list of journeys to be returned by the command
            settings: Settings for the application

        """
        flight_events_repository = AsyncMock(**{"list.return_value": flight_events})
        command = SearchJourneysCommand(
            date=date(2021, 12, 31),
            from_airport="MAD",
            to_airport="BUE",
            flight_events_repository=flight_events_repository,
            settings=settings,
        )
        assert await command.execute() == expected_journeys
