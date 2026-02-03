"""Aggregate company time series into comparison tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

from metrics import METRICS, PERIOD_AXIS

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "company_timeseries.json"
OUTPUT_DIR = ROOT / "output"
OUTPUT_JSON = OUTPUT_DIR / "comparison_table.json"
OUTPUT_CSV = OUTPUT_DIR / "comparison_table.csv"
REPO_ROOT = ROOT.parent
UI_DATA_DIR = REPO_ROOT / "ui" / "data"
UI_OUTPUT_JSON = UI_DATA_DIR / "comparison_table.json"
OUTPUT_METADATA = OUTPUT_DIR / "metadata.json"
UI_METADATA = UI_DATA_DIR / "metadata.json"


def load_company_data(path: Path = DATA_PATH) -> Dict:
    with path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)


def build_rows(data: Dict) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    metrics = [metric.key for metric in METRICS]

    for company in data["companies"]:
        for period in PERIOD_AXIS:
            period_key = str(period)
            series = company["time_series"].get(period_key, {})
            row = {
                "company_id": company["company_id"],
                "company_name": company["company_name"],
                "ipo_year": company["ipo_year"],
                "period": period,
            }
            for metric in metrics:
                row[metric] = series.get(metric)
            row["sources"] = company["sources"]
            rows.append(row)
    return rows


def write_json(rows: Iterable[Dict[str, object]], path: Path = OUTPUT_JSON) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(list(rows), file_handle, ensure_ascii=False, indent=2)


def write_csv(rows: Iterable[Dict[str, object]], path: Path = OUTPUT_CSV) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        return

    fieldnames = [
        "company_id",
        "company_name",
        "ipo_year",
        "period",
        *[metric.key for metric in METRICS],
        "sources",
    ]
    with path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_copy = dict(row)
            row_copy["sources"] = json.dumps(row_copy["sources"], ensure_ascii=False)
            writer.writerow(row_copy)


def write_metadata(path: Path) -> None:
    payload = {
        "metrics": [
            {
                "key": metric.key,
                "label": metric.label,
                "unit": metric.unit,
                "description": metric.description,
            }
            for metric in METRICS
        ],
        "period_axis": PERIOD_AXIS,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, ensure_ascii=False, indent=2)


def main() -> None:
    data = load_company_data()
    rows = build_rows(data)
    write_json(rows)
    write_json(rows, path=UI_OUTPUT_JSON)
    write_csv(rows)
    write_metadata(OUTPUT_METADATA)
    write_metadata(UI_METADATA)


if __name__ == "__main__":
    main()
