"""Flight event repository interface."""

from abc import ABC, abstractmethod

from src.models import FlightEvent


class FlightEventReadRepositoryInterface(ABC):
    """Flight event repository interface."""

    @abstractmethod
    async def list(self) -> list[FlightEvent]:
        """List flight events."""
