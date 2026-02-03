# VC_valuation_comparison

This repository provides a lightweight matching pipeline for comparing venture-backed companies by category, business model, and textual similarity.

## Category taxonomy
- Industry codes follow a simplified Japan Industry Classification-inspired scheme with custom tags.
- Business model categories cover SaaS, marketplace, transaction, ads, and hardware.

## Matching pipeline
The pipeline supports:
1. Attribute ingestion (`InputProfile`)
2. Candidate extraction (industry or tag overlap)
3. Scoring (rule-based + embedding-based)
4. Explainable score breakdown metadata

## Quick start
```python
from matching.models import InputProfile
from matching.pipeline import build_sample_candidates, run_matching_pipeline

profile = InputProfile(
    industry_code="I101",
    tags=["SaaS", "クラウド"],
    business_models=["SaaS"],
    markets=["日本"],
    customer_types=["SMB"],
    description="クラウド運用の自動化を支援するB2B SaaS",
)

companies = build_sample_candidates()
results = run_matching_pipeline(profile, companies)
for result in results:
    print(result.company.name, result.breakdown.total_score, result.breakdown.matched_tags)
```
