"""Connector stub for TDnet."""

from typing import Iterable

from data_ingest.connectors.base import Connector
from data_ingest.normalization import Identifier


class TdnetConnector(Connector):
    source_name = "TDnet"

    def fetch(self) -> Iterable[Identifier]:
        # Placeholder for TDnet scraping/API integration.
        return []
