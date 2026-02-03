"""Common schema definitions for normalized data."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Company:
    company_id: str
    name: str
    securities_code: Optional[str] = None
    corporate_number: Optional[str] = None


@dataclass
class IpoEvent:
    company_id: str
    ipo_date: date
    market: Optional[str] = None
    offer_price: Optional[float] = None


@dataclass
class MAEvent:
    acquirer_company_id: str
    target_company_id: str
    announcement_date: date
    deal_value: Optional[float] = None


@dataclass
class FinancialsPreIpo:
    company_id: str
    period_end: date
    revenue: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None


@dataclass
class MarketDataPostIpo:
    company_id: str
    trade_date: date
    close_price: Optional[float] = None
    market_cap: Optional[float] = None
