# Data ingestion

This module captures data sources, normalization, and loading into a common schema for
valuation comparisons.

## Data sources and acquisition methods

| Source | Acquisition | Formats | Notes |
| --- | --- | --- | --- |
| EDINET | API | XBRL/CSV | Financial reports (有価証券報告書/四半期報告書) |
| TDnet | API | PDF/HTML | Timely disclosures (決算短信/適時開示) |
| Listed company filings | Scraping | HTML/PDF | Issuer IR sites as fallback |
| M&A press releases | Scraping | HTML | Deal announcements |
| 官報 | Scraping | PDF/HTML | Legal events and corporate changes |

## Identifier normalization

Identifiers are normalized using:
- Company name cleanup (remove corp suffixes, normalize whitespace, uppercase)
- Securities codes: digits only
- Corporate number: zero-padded 13 digits
- M&A counterparty: normalized like company names

## Common schema

The pipeline loads into these common tables:
- `companies`
- `events_ipo`
- `events_ma`
- `financials_pre_ipo`
- `market_data_post_ipo`

## Deduplication and entity resolution

Identifiers are matched by normalized name, securities code, corporate number, and
counterparty name when applicable. A resolution index stores canonical IDs.
