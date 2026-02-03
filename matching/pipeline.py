from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from matching.embedding import SimpleTfidfEmbedder
from matching.models import Company, InputProfile, MatchResult, ScoreBreakdown
from matching.rules import RuleWeights, rule_score


DEFAULT_RULE_WEIGHT = 0.6
DEFAULT_EMBEDDING_WEIGHT = 0.4


def build_sample_candidates() -> List[Company]:
    return [
        Company(
            name="CloudOps",
            industry_code="I101",
            tags=["SaaS", "クラウド", "業務効率化"],
            business_model="SaaS",
            market="日本",
            customer_type="SMB",
            description="クラウドでIT運用を自動化するB2B向けSaaS。",
        ),
        Company(
            name="MediLink",
            industry_code="I104",
            tags=["医療", "データ分析", "SaaS"],
            business_model="SaaS",
            market="日本",
            customer_type="エンタープライズ",
            description="医療データの統合分析を提供する医療ITプラットフォーム。",
        ),
        Company(
            name="TradeHub",
            industry_code="I102",
            tags=["マーケットプレイス", "取引仲介", "B2B"],
            business_model="マーケットプレイス",
            market="APAC",
            customer_type="SMB",
            description="製造業向けの部品取引を仲介するB2Bマーケットプレイス。",
        ),
        Company(
            name="PayBridge",
            industry_code="I103",
            tags=["決済", "金融", "API"],
            business_model="トランザクション",
            market="北米",
            customer_type="プラットフォーム",
            description="API連携型の決済インフラを提供するフィンテック企業。",
        ),
    ]


def extract_candidates(profile: InputProfile, companies: Iterable[Company]) -> List[Company]:
    candidates: List[Company] = []
    tag_set = {tag.lower() for tag in profile.tags}
    for company in companies:
        has_tag_overlap = any(tag.lower() in tag_set for tag in company.tags)
        if company.industry_code == profile.industry_code or has_tag_overlap:
            candidates.append(company)
    return candidates


def score_companies(
    profile: InputProfile,
    companies: Iterable[Company],
    rule_weight: float = DEFAULT_RULE_WEIGHT,
    embedding_weight: float = DEFAULT_EMBEDDING_WEIGHT,
    rule_weights: RuleWeights | None = None,
) -> List[MatchResult]:
    company_list = list(companies)
    embedder = SimpleTfidfEmbedder([profile.description] + [c.description for c in company_list])

    results: List[MatchResult] = []
    for company in company_list:
        rule_score_value, matches, feature_weights = rule_score(profile, company, rule_weights)
        embedding_result = embedder.similarity(profile.description, company.description)

        total_score = (rule_score_value * rule_weight) + (embedding_result.score * embedding_weight)
        breakdown = ScoreBreakdown(
            total_score=round(total_score, 4),
            rule_score=round(rule_score_value, 4),
            embedding_score=round(embedding_result.score, 4),
            matched_tags=matches["matched_tags"],
            matched_markets=matches["matched_markets"],
            matched_customer_types=matches["matched_customer_types"],
            matched_business_models=matches["matched_business_models"],
            matched_industry=matches["matched_industry"],
            similarity_terms=embedding_result.shared_terms,
            feature_weights=feature_weights,
        )
        metadata = {
            "rule_score_detail": str(asdict(breakdown)),
            "rule_weight": str(rule_weight),
            "embedding_weight": str(embedding_weight),
        }
        results.append(MatchResult(company=company, breakdown=breakdown, metadata=metadata))

    return sorted(results, key=lambda result: result.breakdown.total_score, reverse=True)


def run_matching_pipeline(
    profile: InputProfile,
    companies: Iterable[Company],
    rule_weight: float = DEFAULT_RULE_WEIGHT,
    embedding_weight: float = DEFAULT_EMBEDDING_WEIGHT,
) -> List[MatchResult]:
    candidates = extract_candidates(profile, companies)
    if not candidates:
        return []
    return score_companies(
        profile,
        candidates,
        rule_weight=rule_weight,
        embedding_weight=embedding_weight,
    )
