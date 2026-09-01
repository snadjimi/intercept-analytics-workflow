"""Business rules used by the synthetic lost-customer example."""

from __future__ import annotations

import pandas as pd


def find_lost_customers(
    customers: pd.DataFrame,
    quiet_days: int = 60,
    minimum_account_age_days: int = 90,
) -> pd.Series:
    """Return a deterministic 0/1 lost-customer label for each input row.

    A customer is considered lost when they have been inactive longer than the
    configured waiting period and the account is old enough to judge. Missing
    account age is treated as a new/unknown account rather than producing a null
    prediction.
    """
    inactivity = pd.to_numeric(customers["last_active_days"], errors="coerce").fillna(0)
    account_age = pd.to_numeric(
        customers["account_age_days"], errors="coerce"
    ).fillna(0)

    lost = (inactivity > quiet_days) & (account_age >= minimum_account_age_days)
    return lost.astype(int).rename("predicted_lost")
