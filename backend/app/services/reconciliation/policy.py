from __future__ import annotations

import pandas as pd

from app.schemas import ObservedTotalsInclusionPolicy
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.base import build_reconcilable_payroll_base


def apply_observed_totals_policy(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
    policy: ObservedTotalsInclusionPolicy | None = None,
) -> pd.DataFrame:
    resolved_policy = policy or ObservedTotalsInclusionPolicy()
    base = build_reconcilable_payroll_base(
        payroll_source,
        concept_master_source,
        target_period=target_period,
    ).reconciliable_base.copy()

    include_mask = pd.Series(True, index=base.index)

    if resolved_policy.include_valid_mapped_records:
        include_mask &= base["is_valid_record"] & ~base["is_unmapped_concept"]

    if resolved_policy.exclude_out_of_period_records:
        include_mask &= ~base["is_out_of_period"]

    if resolved_policy.exclude_unmapped_records:
        include_mask &= ~base["is_unmapped_concept"]

    if resolved_policy.exclude_invalid_records:
        include_mask &= base["is_valid_record"]

    base["include_in_observed_totals"] = include_mask
    base["exclusion_reasons_for_observed"] = [
        _collect_exclusion_reasons(row)
        for _, row in base.iterrows()
    ]

    return base


def _collect_exclusion_reasons(row: pd.Series) -> list[str]:
    reasons: list[str] = []

    if not bool(row["is_valid_record"]):
        reasons.append("invalid_record")
    if bool(row["is_unmapped_concept"]):
        reasons.append("unmapped_concept")
    if bool(row["is_out_of_period"]):
        reasons.append("out_of_period")

    return reasons
