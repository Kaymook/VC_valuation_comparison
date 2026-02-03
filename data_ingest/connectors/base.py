"""Base connector interfaces."""

from abc import ABC, abstractmethod
from typing import Iterable

from data_ingest.normalization import Identifier


class Connector(ABC):
    """Base connector interface for source-specific ingestion."""

    @abstractmethod
    def fetch(self) -> Iterable[Identifier]:
        """Yield raw identifiers discovered from the source."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the data source."""
