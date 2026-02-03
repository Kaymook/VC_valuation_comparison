from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from matching.models import Company, InputProfile


@dataclass(frozen=True)
class RuleWeights:
    industry: float = 0.2
    tags: float = 0.25
    business_model: float = 0.2
    market: float = 0.2
    customer_type: float = 0.15


def _match_list(candidates: Iterable[str], targets: Iterable[str]) -> List[str]:
    target_set = {item.lower() for item in targets}
    return [item for item in candidates if item.lower() in target_set]


def rule_score(
    profile: InputProfile,
    company: Company,
    weights: RuleWeights | None = None,
) -> Tuple[float, Dict[str, List[str]], Dict[str, float]]:
    weights = weights or RuleWeights()
    matched_tags = _match_list(company.tags, profile.tags)
    matched_markets = _match_list([company.market], profile.markets)
    matched_customer_types = _match_list([company.customer_type], profile.customer_types)
    matched_business_models = _match_list([company.business_model], profile.business_models)
    matched_industry = company.industry_code == profile.industry_code

    feature_matches = {
        "matched_tags": matched_tags,
        "matched_markets": matched_markets,
        "matched_customer_types": matched_customer_types,
        "matched_business_models": matched_business_models,
        "matched_industry": matched_industry,
    }

    score = 0.0
    if matched_industry:
        score += weights.industry
    if matched_tags:
        score += weights.tags
    if matched_business_models:
        score += weights.business_model
    if matched_markets:
        score += weights.market
    if matched_customer_types:
        score += weights.customer_type

    feature_weights = {
        "industry": weights.industry,
        "tags": weights.tags,
        "business_model": weights.business_model,
        "market": weights.market,
        "customer_type": weights.customer_type,
    }

    return score, feature_matches, feature_weights
