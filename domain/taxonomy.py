from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class IndustryCategory:
    code: str
    name: str
    tags: List[str]


JIC_CATEGORIES: Dict[str, IndustryCategory] = {
    "I101": IndustryCategory(
        code="I101",
        name="ソフトウェア・SaaS",
        tags=["SaaS", "クラウド", "B2B", "業務効率化"],
    ),
    "I102": IndustryCategory(
        code="I102",
        name="Eコマース・マーケットプレイス",
        tags=["EC", "マーケットプレイス", "取引仲介", "B2C"],
    ),
    "I103": IndustryCategory(
        code="I103",
        name="フィンテック",
        tags=["決済", "融資", "B2B", "B2C"],
    ),
    "I104": IndustryCategory(
        code="I104",
        name="ヘルスケア・医療IT",
        tags=["医療", "データ分析", "B2B", "規制"],
    ),
}

BUSINESS_MODEL_CATEGORIES: Dict[str, List[str]] = {
    "SaaS": ["サブスクリプション", "ARR", "チャーン"],
    "マーケットプレイス": ["GMV", "マッチング", "取引手数料"],
    "トランザクション": ["決済", "手数料", "取引量"],
    "広告": ["広告", "MAU", "CPM"],
    "ハードウェア": ["デバイス販売", "製造"],
}


def known_industry_codes() -> List[str]:
    return list(JIC_CATEGORIES.keys())


def known_business_models() -> List[str]:
    return list(BUSINESS_MODEL_CATEGORIES.keys())
