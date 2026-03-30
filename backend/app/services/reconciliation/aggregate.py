from __future__ import annotations

import pandas as pd

from app.schemas import ObservedTotalsInclusionPolicy, ObservedTotalsResult
from app.schemas.reconciliation import DataFrameLike
from app.services.reconciliation.policy import apply_observed_totals_policy


def build_observed_totals(
    payroll_source: DataFrameLike | pd.DataFrame,
    concept_master_source: DataFrameLike,
    target_period: str,
    policy: ObservedTotalsInclusionPolicy | None = None,
    segment_by_legal_entity: bool = False,
) -> ObservedTotalsResult:
    base = apply_observed_totals_policy(
        payroll_source,
        concept_master_source,
        target_period=target_period,
        policy=policy,
    )

    included = base.loc[base["include_in_observed_totals"]].copy()
    group_columns = [
        "payroll_period_normalized",
        "concept_code_normalized",
        "concept_name_normalized",
    ]
    if segment_by_legal_entity:
        group_columns.append("legal_entity")

    observed_totals = (
        included.groupby(
            group_columns,
            as_index=False,
        )
        .agg(
            observed_amount=("amount_for_aggregation", "sum"),
            record_count=("record_id", "count"),
            employee_count=("employee_id", "nunique"),
        )
        .rename(columns={"payroll_period_normalized": "period"})
        .sort_values(["period", "concept_code_normalized"], ignore_index=True)
    )

    return ObservedTotalsResult(
        observed_totals=observed_totals,
        total_groups=len(observed_totals),
        segmented_by_legal_entity=segment_by_legal_entity,
    )
