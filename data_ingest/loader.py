"""Load normalized data into common schema collections."""

from dataclasses import dataclass, field
from typing import Dict, List

from data_ingest.schema import (
    Company,
    FinancialsPreIpo,
    IpoEvent,
    MAEvent,
    MarketDataPostIpo,
)


@dataclass
class CommonSchemaStore:
    companies: Dict[str, Company] = field(default_factory=dict)
    events_ipo: List[IpoEvent] = field(default_factory=list)
    events_ma: List[MAEvent] = field(default_factory=list)
    financials_pre_ipo: List[FinancialsPreIpo] = field(default_factory=list)
    market_data_post_ipo: List[MarketDataPostIpo] = field(default_factory=list)

    def add_company(self, company: Company) -> None:
        self.companies[company.company_id] = company
