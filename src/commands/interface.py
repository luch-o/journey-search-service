"""Command interface."""

from abc import ABC, abstractmethod
from typing import Any


class CommandInterface(ABC):
    """Command interface definition."""

    @abstractmethod
    async def execute(self) -> Any:  # noqa: ANN401
        """Execute the command."""
