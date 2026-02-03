"""Orchestrates source connectors, normalization, and loading."""

from dataclasses import dataclass, field
from typing import Iterable, List

from data_ingest.connectors.edinet import EdinetConnector
from data_ingest.connectors.ir_sites import IrSiteConnector
from data_ingest.connectors.kanpo import KanpoConnector
from data_ingest.connectors.ma_press import MAPressConnector
from data_ingest.connectors.tdnet import TdnetConnector
from data_ingest.dedup import resolve_company
from data_ingest.loader import CommonSchemaStore
from data_ingest.normalization import Identifier
from data_ingest.sources import DATA_SOURCES


@dataclass
class IngestPipeline:
    connectors: List = field(
        default_factory=lambda: [
            EdinetConnector(),
            TdnetConnector(),
            IrSiteConnector(),
            MAPressConnector(),
            KanpoConnector(),
        ]
    )
    store: CommonSchemaStore = field(default_factory=CommonSchemaStore)

    def list_sources(self):
        return DATA_SOURCES

    def collect_identifiers(self) -> Iterable[Identifier]:
        for connector in self.connectors:
            for identifier in connector.fetch():
                yield identifier

    def load(self) -> CommonSchemaStore:
        index = {}
        for identifier in self.collect_identifiers():
            resolve_company(identifier, index, self.store.companies)
        return self.store
