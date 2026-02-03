"""Connector stub for EDINET API."""

from typing import Iterable

from data_ingest.connectors.base import Connector
from data_ingest.normalization import Identifier


class EdinetConnector(Connector):
    source_name = "EDINET"

    def fetch(self) -> Iterable[Identifier]:
        # Placeholder for EDINET API integration.
        return []
