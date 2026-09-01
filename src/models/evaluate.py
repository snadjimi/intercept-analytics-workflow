"""Evaluate the synthetic business rule against a fixed labelled sample."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import yaml

from src.features import find_lost_customers


def load_config(path: Path = Path("config/client.yml")) -> dict[str, int]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def evaluate(customers_path: Path, baseline_path: Path, out_path: Path) -> dict:
    customers = pd.read_csv(customers_path)
    config = load_config()

    predictions = find_lost_customers(
        customers,
        quiet_days=int(config["quiet_days"]),
        minimum_account_age_days=int(config["minimum_account_age_days"]),
    )
    accuracy = round(float((predictions == customers["actual_lost"]).mean()), 2)
    customers_lost = round(float(predictions.mean()), 3)

    with baseline_path.open(encoding="utf-8") as handle:
        baseline = json.load(handle)

    result = {
        "last_time": {
            "accuracy": float(baseline["accuracy"]),
            "quiet_days": int(baseline["quiet_days"]),
        },
        "this_change": {
            "accuracy": accuracy,
            "quiet_days": int(config["quiet_days"]),
            "customers_lost": customers_lost,
        },
        "lowest_allowed": float(baseline["lowest_allowed"]),
        "sample_rows": int(len(customers)),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(
        f"accuracy {baseline['accuracy']:.2f} -> {accuracy:.2f}; "
        f"quiet days {baseline['quiet_days']} -> {config['quiet_days']}"
    )

    if accuracy < float(baseline["lowest_allowed"]):
        raise SystemExit(
            f"score gate failed: {accuracy:.2f} < {baseline['lowest_allowed']:.2f}"
        )

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    evaluate(args.customers, args.baseline, args.out)


if __name__ == "__main__":
    main()
