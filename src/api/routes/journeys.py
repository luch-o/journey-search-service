"""Routes for the API."""

import logging
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException

from src.commands import SearchJourneysCommand
from src.core.dependencies import AppSettings
from src.models import Airport, Journey
from src.repositories.flight_events import (
    FlightEventRetrievalError,
    FlightEventsAPIRepository,
)

router = APIRouter()


@router.get("/search")
async def search(
    date: date,
    from_airport: Annotated[Airport, Query(alias="from")],
    to_airport: Annotated[Airport, Query(alias="to")],
    settings: AppSettings,
) -> list[Journey]:
    """GET /search.

    Search for journeys between two airports on a given date.

    Args:
        date: Query parameter. The date to search for journeys.
        from_airport: Query parameter. The airport to depart from.
        to_airport: Query parameter. The airport to arrive to.
        settings: The application settings. From dependency injection.

    Returns:
        A list of journeys between the two airports

    """
    flight_events_repository = FlightEventsAPIRepository(settings)
    command = SearchJourneysCommand(
        date=date,
        from_airport=from_airport,
        to_airport=to_airport,
        flight_events_repository=flight_events_repository,
        settings=settings,
    )
    try:
        return await command.execute()
    except FlightEventRetrievalError as e:
        logging.error(f"Failed to retrieve flight events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve flight events",
        ) from e
