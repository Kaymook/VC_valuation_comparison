"""Deduplication and entity resolution utilities."""

from dataclasses import dataclass
from typing import Dict, Iterable, List

from data_ingest.normalization import Identifier, candidate_keys, normalize_identifier
from data_ingest.schema import Company


@dataclass
class EntityResolutionResult:
    canonical_company_id: str
    matched_keys: List[str]


def resolve_company(
    identifier: Identifier,
    index: Dict[str, str],
    companies: Dict[str, Company],
) -> EntityResolutionResult:
    normalized = normalize_identifier(identifier)
    keys = list(candidate_keys(normalized))
    for key in keys:
        if key in index:
            return EntityResolutionResult(index[key], keys)

    company_id = f"company_{len(companies) + 1:05d}"
    companies[company_id] = Company(
        company_id=company_id,
        name=normalized.company_name,
        securities_code=normalized.securities_code,
        corporate_number=normalized.corporate_number,
    )
    for key in keys:
        index[key] = company_id
    return EntityResolutionResult(company_id, keys)


def build_resolution_index(identifiers: Iterable[Identifier]) -> Dict[str, str]:
    index: Dict[str, str] = {}
    companies: Dict[str, Company] = {}
    for identifier in identifiers:
        resolve_company(identifier, index, companies)
    return index
