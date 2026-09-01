"""A deliberately small data contract for the committed synthetic sample."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "customer_id",
    "last_active_days",
    "account_age_days",
    "actual_lost",
    "segment",
}


def validate(path: Path) -> None:
    """Fail loudly when the input no longer matches the pipeline's assumptions."""
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("sample data is empty")

    if df["customer_id"].duplicated().any():
        raise ValueError("customer_id must be unique")

    if df["last_active_days"].isna().any():
        raise ValueError("last_active_days may not be null")

    if (df["last_active_days"] < 0).any():
        raise ValueError("last_active_days may not be negative")

    if not set(df["actual_lost"].dropna().unique()).issubset({0, 1}):
        raise ValueError("actual_lost must contain only 0/1")

    account_age_null_rate = float(df["account_age_days"].isna().mean())
    if account_age_null_rate > 0.10:
        raise ValueError(
            f"account_age_days null rate {account_age_null_rate:.1%} exceeds 10%"
        )

    print(
        f"contract passed: {len(df)} rows, "
        f"account_age null rate {account_age_null_rate:.1%}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    validate(args.csv)


if __name__ == "__main__":
    main()
