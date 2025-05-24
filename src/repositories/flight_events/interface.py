"""Flight event repository interface."""

from abc import ABC, abstractmethod

from src.models import FlightEvent


class FlightEventReadRepository(ABC):
    """Flight event repository interface."""

    @abstractmethod
    def list(self) -> list[FlightEvent]:
        """List flight events."""
