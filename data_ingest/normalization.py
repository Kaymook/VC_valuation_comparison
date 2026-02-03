"""Identifier normalization and entity matching rules."""

from dataclasses import dataclass
import re
from typing import Iterable, Optional


CORP_SUFFIXES = [
    "株式会社",
    "(株)",
    "（株）",
    "Inc.",
    "Inc",
    "Ltd.",
    "Ltd",
    "Co., Ltd.",
    "Co.,Ltd.",
]


@dataclass(frozen=True)
class Identifier:
    company_name: str
    securities_code: Optional[str] = None
    corporate_number: Optional[str] = None
    counterparty: Optional[str] = None


def normalize_company_name(name: str) -> str:
    cleaned = name.strip()
    for suffix in CORP_SUFFIXES:
        cleaned = cleaned.replace(suffix, "")
    cleaned = re.sub(r"[\s\u3000]+", " ", cleaned)
    return cleaned.strip().upper()


def normalize_securities_code(code: Optional[str]) -> Optional[str]:
    if not code:
        return None
    digits = re.sub(r"\D", "", code)
    return digits if digits else None


def normalize_corporate_number(number: Optional[str]) -> Optional[str]:
    if not number:
        return None
    digits = re.sub(r"\D", "", number)
    return digits.zfill(13) if digits else None


def normalize_counterparty(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    return normalize_company_name(name)


def normalize_identifier(identifier: Identifier) -> Identifier:
    return Identifier(
        company_name=normalize_company_name(identifier.company_name),
        securities_code=normalize_securities_code(identifier.securities_code),
        corporate_number=normalize_corporate_number(identifier.corporate_number),
        counterparty=normalize_counterparty(identifier.counterparty),
    )


def candidate_keys(identifier: Identifier) -> Iterable[str]:
    normalized = normalize_identifier(identifier)
    keys = [normalized.company_name]
    if normalized.securities_code:
        keys.append(f"securities:{normalized.securities_code}")
    if normalized.corporate_number:
        keys.append(f"corp:{normalized.corporate_number}")
    if normalized.counterparty:
        keys.append(f"counterparty:{normalized.counterparty}")
    return keys
