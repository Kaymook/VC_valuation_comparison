"""Source registry and acquisition methods."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DataSource:
    name: str
    description: str
    acquisition_method: str
    expected_format: str
    notes: str


DATA_SOURCES: List[DataSource] = [
    DataSource(
        name="EDINET",
        description="Financial reports (有価証券報告書/四半期報告書) for listed firms.",
        acquisition_method="API",
        expected_format="XBRL/CSV",
        notes="Use EDINET API to download XBRL; parse into normalized tables.",
    ),
    DataSource(
        name="TDnet",
        description="Timely disclosure filings (決算短信/適時開示).",
        acquisition_method="API",
        expected_format="PDF/HTML",
        notes="TDnet provides downloads; parse metadata and text.",
    ),
    DataSource(
        name="Listed company filings",
        description="Financial statements and press releases on issuer IR sites.",
        acquisition_method="Scraping",
        expected_format="HTML/PDF",
        notes="Used as a fallback when EDINET/TDnet data is missing.",
    ),
    DataSource(
        name="M&A press releases",
        description="Press releases on acquisitions and exits.",
        acquisition_method="Scraping",
        expected_format="HTML",
        notes="Capture counterparty and deal size disclosures.",
    ),
    DataSource(
        name="官報",
        description="Official gazette for corporate events (bankruptcies, mergers).",
        acquisition_method="Scraping",
        expected_format="PDF/HTML",
        notes="Supplemental source for entity changes and legal events.",
    ),
]
