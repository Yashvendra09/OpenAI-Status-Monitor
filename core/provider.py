from abc import ABC, abstractmethod
from typing import List
from models import IncidentEvent


class StatusProvider(ABC):
    """
    Abstract base class for any status page provider.
    Makes system extensible to 100+ providers.
    """

    @abstractmethod
    async def fetch(self, fetcher):
        """Fetch raw data from provider"""
        pass

    @abstractmethod
    def parse(self, data) -> List[IncidentEvent]:
        """Parse provider response into standardized IncidentEvent objects"""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return provider name"""
        pass