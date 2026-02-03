"""Metric definitions and period axis for VC valuation comparisons."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MetricDefinition:
    key: str
    label: str
    unit: str
    description: str


PRE_IPO_YEARS = 3
POST_IPO_YEARS = 2

PERIOD_AXIS: List[int] = list(range(-PRE_IPO_YEARS, POST_IPO_YEARS + 1))

METRICS: List[MetricDefinition] = [
    MetricDefinition(
        key="revenue",
        label="売上",
        unit="億円",
        description="売上高（連結・単体の代表値）",
    ),
    MetricDefinition(
        key="net_income",
        label="純利益",
        unit="億円",
        description="親会社株主に帰属する当期純利益",
    ),
    MetricDefinition(
        key="operating_income",
        label="営業利益",
        unit="億円",
        description="営業利益（EBIT）",
    ),
    MetricDefinition(
        key="market_cap",
        label="時価総額",
        unit="億円",
        description="株価 × 発行済株式数",
    ),
    MetricDefinition(
        key="tam",
        label="TAM",
        unit="億円",
        description="Total Addressable Market",
    ),
    MetricDefinition(
        key="sam",
        label="SAM",
        unit="億円",
        description="Serviceable Available Market",
    ),
    MetricDefinition(
        key="som",
        label="SOM",
        unit="億円",
        description="Serviceable Obtainable Market",
    ),
]
