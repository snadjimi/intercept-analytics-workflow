from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.contracts.validate import validate


def test_contract_rejects_duplicate_customers(tmp_path: Path):
    path = tmp_path / "customers.csv"
    pd.DataFrame(
        {
            "customer_id": [1, 1],
            "last_active_days": [10, 20],
            "account_age_days": [100, 100],
            "actual_lost": [0, 0],
            "segment": ["SMB", "SMB"],
        }
    ).to_csv(path, index=False)

    with pytest.raises(ValueError, match="customer_id must be unique"):
        validate(path)
