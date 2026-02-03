"""Connector stub for 官報 (official gazette)."""

from typing import Iterable

from data_ingest.connectors.base import Connector
from data_ingest.normalization import Identifier


class KanpoConnector(Connector):
    source_name = "官報"

    def fetch(self) -> Iterable[Identifier]:
        # Placeholder for 官報 scraping.
        return []
