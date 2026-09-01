from __future__ import annotations

import pandas as pd

from src.features import find_lost_customers


def frame(last_active_days, account_age_days=365):
    return pd.DataFrame(
        {
            "last_active_days": last_active_days,
            "account_age_days": [account_age_days] * len(last_active_days),
        }
    )


def test_waiting_period_boundary_is_exclusive():
    labels = find_lost_customers(frame([59, 60, 61]), quiet_days=60)
    assert labels.tolist() == [0, 0, 1]


def test_missing_account_age_never_produces_null_label():
    customers = pd.DataFrame(
        {"last_active_days": [100, 20], "account_age_days": [None, None]}
    )
    labels = find_lost_customers(customers, quiet_days=60)
    assert labels.notna().all()
    assert labels.tolist() == [0, 0]


def test_new_accounts_are_not_called_lost():
    customers = pd.DataFrame({"last_active_days": [120], "account_age_days": [45]})
    assert find_lost_customers(customers, quiet_days=60).tolist() == [0]


def test_output_has_exactly_one_label_per_input_row():
    customers = frame([10, 20, 70, 90])
    labels = find_lost_customers(customers)
    assert len(labels) == len(customers)
    assert labels.index.equals(customers.index)
