from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Company:
    name: str
    industry_code: str
    tags: List[str]
    business_model: str
    market: str
    customer_type: str
    description: str


@dataclass(frozen=True)
class InputProfile:
    industry_code: str
    tags: List[str]
    business_models: List[str]
    markets: List[str]
    customer_types: List[str]
    description: str


@dataclass(frozen=True)
class ScoreBreakdown:
    total_score: float
    rule_score: float
    embedding_score: float
    matched_tags: List[str] = field(default_factory=list)
    matched_markets: List[str] = field(default_factory=list)
    matched_customer_types: List[str] = field(default_factory=list)
    matched_business_models: List[str] = field(default_factory=list)
    matched_industry: bool = False
    similarity_terms: List[str] = field(default_factory=list)
    feature_weights: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class MatchResult:
    company: Company
    breakdown: ScoreBreakdown
    metadata: Optional[Dict[str, str]] = None
