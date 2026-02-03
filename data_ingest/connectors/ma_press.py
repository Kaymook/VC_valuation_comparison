"""Connector stub for M&A press releases."""

from typing import Iterable

from data_ingest.connectors.base import Connector
from data_ingest.normalization import Identifier


class MAPressConnector(Connector):
    source_name = "M&A press releases"

    def fetch(self) -> Iterable[Identifier]:
        # Placeholder for press release scraping.
        return []
