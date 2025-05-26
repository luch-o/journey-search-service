"""Models that represent business entities."""

from datetime import datetime
from functools import cached_property
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    FieldSerializationInfo,
    computed_field,
    field_serializer,
)

Airport = Annotated[str, Field(pattern=r"^[A-Z]{3}$")]


class FlightEvent(BaseModel):
    """Flight event model."""

    flight_number: str
    from_airport: Airport = Field(serialization_alias="from")
    to_airport: Airport = Field(serialization_alias="to")
    departure_time: datetime
    arrival_time: datetime

    @field_serializer("departure_time", "arrival_time")
    def serialize_datetime(self, dt: datetime, _info: FieldSerializationInfo) -> str:
        """Serialize datetime to established format."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class Journey(BaseModel):
    """Journey model."""

    path: list[FlightEvent]

    @computed_field
    @cached_property
    def connections(self) -> int:
        """Amount of connections between flights."""
        return len(self.path) - 1
