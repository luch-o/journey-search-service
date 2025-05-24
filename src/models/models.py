"""Models that represent business entities."""

from datetime import datetime
from functools import cached_property

from pydantic import BaseModel, computed_field


class FlightEvent(BaseModel):
    """Flight event model."""

    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    departure_airport: str
    arrival_airport: str


class Journey(BaseModel):
    """Journey model."""

    path: list[FlightEvent]

    @computed_field
    @cached_property
    def connections(self) -> int:
        """Amount of connections between flights."""
        return len(self.path) - 1
