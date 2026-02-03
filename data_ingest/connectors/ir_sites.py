"""Connector stub for listed company IR sites."""

from typing import Iterable

from data_ingest.connectors.base import Connector
from data_ingest.normalization import Identifier


class IrSiteConnector(Connector):
    source_name = "Listed company filings"

    def fetch(self) -> Iterable[Identifier]:
        # Placeholder for scraping issuer IR sites.
        return []
